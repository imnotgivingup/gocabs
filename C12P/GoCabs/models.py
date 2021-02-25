from django.db import models

class Customer_detail(models.Model):
    Customer_Id = models.AutoField(primary_key=True)
    C_Name = models.CharField(max_length=200)
    C_Phone_no = models.CharField(max_length=30)
    C_Mail_Id = models.EmailField()
    H_address = models.CharField(max_length=1000)
    Password = models.CharField(max_length=30)
    C_Gender = models.CharField(max_length=30)
    C_DOB = models.DateField()

class Cab_detail(models.Model):
    Cab_Id = models.AutoField(primary_key=True)
    Cab_number = models.CharField(max_length=30)
    Car_model = models.CharField(max_length=30)
    Car_type = models.CharField(max_length=30)

    
class Driver_detail(models.Model):
    Driver_Id = models.AutoField(primary_key=True)
    D_Name = models.CharField(max_length=300)
    D_Phone_no = models.CharField(max_length=30)
    D_Mail_Id = models.EmailField()
    Experience = models.IntegerField()
    Age = models.IntegerField()
    Rides_completed = models.IntegerField()
    D_DOB = models.DateField()
    D_Gender = models.CharField(max_length=30)
    License_no = models.CharField(max_length=30)
    Cab = models.ForeignKey(Cab_detail,to_field="Cab_Id", on_delete=models.CASCADE)
    Region = models.CharField(max_length=500)
    Active = models.IntegerField()
    

class Ride(models.Model):
    Ride_no = models.AutoField(primary_key=True)
    Driver = models.ForeignKey(Driver_detail,to_field="Driver_Id", on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer_detail,to_field="Customer_Id", on_delete=models.CASCADE)
    Source = models.CharField(max_length=300)
    Destination = models.CharField(max_length=300)
    Status = models.CharField(max_length=100)
    Amount = models.DecimalField(max_digits=6, decimal_places=2)
    Booking_time = models.TimeField()
    Date_book = models.DateField()
    Reviewed = models.IntegerField()
    
    
class Review(models.Model):
    Review_no = models.AutoField(primary_key=True)
    Customer = models.ForeignKey(Customer_detail,to_field="Customer_Id", on_delete=models.CASCADE)
    Driver = models.ForeignKey(Driver_detail,to_field="Driver_Id", on_delete=models.CASCADE)
    Ride_no = models.ForeignKey(Ride,to_field="Ride_no", on_delete=models.CASCADE,db_column='Ride_no')
    Stars = models.DecimalField(max_digits=4, decimal_places=2)


    
class Cab_location(models.Model):
    Serial_no = models.AutoField(primary_key=True)
    Cab = models.ForeignKey(Cab_detail,to_field="Cab_Id", on_delete=models.CASCADE)
    Area = models.CharField(max_length=5000)
    Zone = models.CharField(max_length=50)
    On_trip_status = models.CharField(max_length=100)

#db_column='' To specify column name    
