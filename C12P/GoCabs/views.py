from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm,SignupForm,DashForm
from django.db import connection
from .models import *
from datetime import datetime, timedelta
import random


def index(request):
  #Company home page
  if request.session.has_key('Usr'):
    #Deleting session variable
    del request.session['Usr']
  return render(request,"index.html")






def login(request):
  #Login page
  if request.method == 'POST':
        form = LoginForm(request.POST)
        #Form Validation
        if form.is_valid():
            cursor=connection.cursor()
            try:              
              cursor.execute('Select Password from gocabs_customer_detail where C_Mail_Id =\''+form.cleaned_data['email']+"\'")
              y=cursor.fetchall()
              if y[0][0]==form.cleaned_data['psd']:
                #Password validation and starting user session
                request.session['Usr'] = form.cleaned_data['email']
                return redirect("../dash")
              else:
                #Wrong Password
                return render(request,"error.html",{'merror':"Recheck creds",'serror':"Wrong Password"})
            except:
              #Invalid Email
              return render(request,"error.html",{'merror':"Recheck creds",'serror':"Invalid Email"})
  elif request.session.has_key('Usr'):
    #If already logged in
    return redirect("../dash")
  #GET request
  return render(request,"login.html")





def signup(request):
  #Signup page
  if request.method == 'POST':
        #Form validation
        form = SignupForm(request.POST)
        if form.is_valid():
            #Match password confirmation
            if form.cleaned_data['psd1']==form.cleaned_data['psd2']:
              cursor=connection.cursor()
              cursor.execute("SELECT C_Mail_Id from gocabs_customer_detail where C_Mail_Id=\'"+form.cleaned_data['email']+"\'")
              val=cursor.fetchall()
              if val:
                #Already exists
                return render(request,"error.html",{'merror':"Email already exists",'serror':"Please login to continue"})
              lst=Customer_detail()
              lst.C_Name=form.cleaned_data['username']
              lst.C_Mail_Id=form.cleaned_data['email']
              lst.H_address=form.cleaned_data['adress']
              lst.Password=form.cleaned_data['psd1']
              lst.C_Gender=form.cleaned_data['gender']
              lst.C_DOB=form.cleaned_data['dob']
              lst.C_Phone_no=form.cleaned_data['pno']
              lst.save()            
              request.session['Usr'] = form.cleaned_data['email']
              return redirect("../dash")
        else:
          #Invalid data
          return render(request,"error.html",{'merror':"Recheck creds",'serror':"Invalid data. Date format YYYY-MM-DD. Email should end with .com"})
  #GET request
  return render(request,"signup.html")





def dash(request):
  if request.session.has_key('Usr'):
    usr = request.session.get('Usr')
    cursor=connection.cursor()
    #Obtain customer name
    cursor.execute('select C_Name from gocabs_customer_detail where C_Mail_Id=\''+usr+'\'')  
    x=cursor.fetchall()
    data_dict = {'Usr': x[0][0]}
    if request.method == 'POST':
    #Process booking data
      form = DashForm(request.POST)
      if form.is_valid():
        time=form.cleaned_data['time']
        #Converting 12hr to 24hr format
        if time[5:]=="PM":
          if int(time[:2])==12:
            time=str(int(time[:2]))+":"+str(time[3:5])
          else:
            time=str(int(time[:2])+12)+":"+str(time[3:5])
        date=datetime.now()
        date=datetime(date.year, date.month, date.day, int(time[:2]),int(time[3:5]))
        now=datetime.now()
        #Checking if cab booked is atleast 30 minutes from now
        if (date-now).total_seconds()//60>=30:
          zone=form.cleaned_data['zone']
          sor=form.cleaned_data['source']
          des=form.cleaned_data['destination']
          typ=form.cleaned_data['typ']
          cursor.execute("select * from gocabs_cab_location a, gocabs_cab_detail b,gocabs_driver_detail c where a.Cab_id=b.Cab_id and a.Cab_id=c.Cab_id and on_trip_status=\"N\" and car_type=\""+typ+"\" and active=1 and zone=\""+zone+"\";")
          data=cursor.fetchall()
          try:
            #Randomly selecting closest available driver
            i=random.randint(0,len(data)-1)
          except:
            #If no drivers available
            return render(request,"error.html",{'merror':"Sorry!",'serror':"No drivers available at the moment, we'll get back to you later :("})
          #Selecting the driver and assigning ride values
          data=data[i]
          dname=data[10]
          cabno=data[6]
          cabty=data[8]+" "+data[7]
          cursor.execute('select Customer_id from gocabs_customer_detail where C_Mail_Id=\''+usr+'\'')
          cid=cursor.fetchall()[0][0]
          did=data[9]
          cursor.execute('select a.cab_id from gocabs_cab_location a, gocabs_driver_detail b where a.cab_id=b.cab_id and Driver_id='+str(did))
          cabid=cursor.fetchall()[0][0]
          #Finalised ride details
          bdetails={'cabid':cabid,'cid':cid,'did':did,'sor':sor,'des':des,'time':str(time),'dname':dname,'cabno':cabno,'cabty':cabty,'date':str(date)}
          request.session['bdetails']=bdetails
          return redirect("../cbooking")
        else:
          #Invalid time
          return render(request,"error.html",{'merror':"Invalid data",'serror':"Check time. It must be atleast half hour from now."})
      else:
        #Empty form
        return render(request,"error.html",{'merror':"Invalid data",'serror':"Please fill in all the fields."})
    else:
      #GET request
      return render(request,"dash.html",data_dict)
  else:
    #Not Logged in
    return redirect("../login")


def booked(request):
  #Confirmed page
  if not request.session.has_key('Usr'):
    return redirect("../login")
  cursor=connection.cursor()
  bdetails=request.session['bdetails']
  date=datetime.now()
  #Update ride and reviews table.
  cursor.execute('insert into gocabs_ride(Source,Destination,Status,Amount,Booking_time,Date_book,Reviewed,Customer_id,Driver_id) values (\'{}\',\'{}\',\'{}\',{},\'{}\',\'{}\',{},{},{})'.format(bdetails['sor'],bdetails['des'],"Not Completed",0,bdetails['time'],str(date.year)+"-"+str(date.month)+"-"+str(date.day),0,bdetails['cid'],bdetails['did']))
  cursor.execute('select max(ride_no) from gocabs_ride')
  rideno=cursor.fetchall()
  rideno=rideno[0][0]
  cursor.execute('insert into gocabs_review(Stars,Customer_id,Driver_id,Ride_no) values({},{},{},{})'.format(5,bdetails['cid'],bdetails['did'],rideno))
  cursor.execute('update gocabs_cab_location set On_Trip_Status = \"Y\" where Cab_id='+str(bdetails['cabid']))
  connection.commit()
  return render(request,"booked.html",request.session['bdetails'])


def cbooking(request):
  #Confirmation page
  if not request.session.has_key('Usr'):
    return redirect("../login")
  bdetails=request.session['bdetails']  
  return render(request,"cbooking.html",bdetails)



def insval(request):
  #Inserting demonstration values
  cursor=connection.cursor()
  fr=open('data.txt','r')
  txt=fr.readline()
  while txt:
    cursor.execute(txt[:len(txt)-1])
    txt=fr.readline()
  html = "<html><body>Data Inserted!!</body></html>"
  return HttpResponse(html)

def tripstatus(request):
  #Make cab drivers available (Demonstration purpose)
  cursor=connection.cursor()
  cursor.execute('update gocabs_cab_location set on_trip_status=\"N\"')
  html = "<html><body>Trip status changed!!</body></html>"
  return HttpResponse(html)

def reviews(request):
  #Reviews table
  if not request.session.has_key('Usr'):
    return redirect("../login")
  cursor=connection.cursor()
  if request.method=="POST":
    #Updating stars
    if request.POST['stars'] not in ('1','2','3','4','5'):
      #Invalid stars
      return render(request,"error.html",{'merror':"Invalid data",'serror':"Stars must be between 1 and 5."})
    cursor.execute('update gocabs_review set stars='+str(request.POST['stars'])+" where review_no="+request.POST['edit'][7:])
    connection.commit()
  #GET request
  cursor.execute("Select * from gocabs_review where customer_id=(select customer_id from gocabs_customer_detail where C_Mail_Id=\""+request.session['Usr']+"\");")
  data=cursor.fetchall()
  l=[]
  for i in data:
    l.append(list(i))
  for i in range(len(l)):
    cursor.execute("select date_book from gocabs_ride where ride_no=(select ride_no from gocabs_review where review_no="+str(l[i][0])+")")
    dater=cursor.fetchall()
    l[i].append('Update '+str(l[i][0]))
    l[i].append(dater[0][0])
    l[i][0]=i+1
  return render(request,"reviews.html",{'data':l})


def rides(request):
  cursor=connection.cursor()
  if not request.session.has_key('Usr'):
    return redirect("../login")
  if request.method=="POST":
    #Deleting rides (Completed or Incomplete)
    cursor.execute('select driver_id from gocabs_ride where Ride_no='+request.POST['edit'][7:])
    did=cursor.fetchall()
    did=did[0][0]
    cursor.execute('SELECT a.cab_id from gocabs_driver_detail a, gocabs_cab_location b where a.cab_id= b.cab_id and driver_id=' + str(did))
    cabid=cursor.fetchall()
    cabid=cabid[0][0]
    cursor.execute('select status from gocabs_ride where Ride_no='+request.POST['edit'][7:])
    st=cursor.fetchall()
    st=st[0][0]
    if st=="Not Completed":
      #If ride is incomplete, driver availability status is made true.
      cursor.execute('update gocabs_cab_location set on_trip_status=\"N\" where cab_id='+str(cabid))
    cursor.execute('delete from gocabs_review where Ride_no='+request.POST['edit'][7:])
    cursor.execute('delete from gocabs_ride where Ride_no='+request.POST['edit'][7:])
    connection.commit()
  #GET request
  cursor.execute("Select * from gocabs_ride where customer_id=(select customer_id from gocabs_customer_detail where C_Mail_Id=\""+request.session['Usr']+"\");")
  data=cursor.fetchall()
  l=[]
  for i in data:
    l.append(list(i))
  for i in range(len(l)):
    l[i].append('Delete '+str(l[i][0]))
    l[i][0]=i+1
  return render(request,"rides.html",{'data':l})
  

def error(request):
  #Error handling
  return render(request,"error.html",{'merror':"404.",'serror':"Page not found"})
