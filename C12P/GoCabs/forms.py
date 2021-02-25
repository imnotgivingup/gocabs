from django import forms

class LoginForm(forms.Form):
    email=forms.EmailField(label='E-Mail')
    psd=forms.CharField(widget = forms.PasswordInput())

class SignupForm(forms.Form):
    username=forms.CharField(label='Username', max_length=100)
    email=forms.EmailField(label='E-Mail')
    psd1=forms.CharField(widget = forms.PasswordInput())
    psd2=forms.CharField(widget = forms.PasswordInput())
    adress=forms.CharField(label='Adress', max_length=1000)
    dob=forms.DateField(label='Date',widget=forms.widgets.DateInput(format="%Y-%m-%d"))
    gender=forms.CharField(label='Gender', max_length=10)
    pno=forms.CharField(label='Phone Number', max_length=15)

class DashForm(forms.Form):
    name=forms.CharField(label='Name', max_length=100)
    phone=forms.CharField(label='Phone Number', max_length=15)
    source=forms.CharField(label='Source', max_length=1000)
    destination=forms.CharField(label='Destination', max_length=1000)
    zone=forms.CharField(label='Phone Number', max_length=15)
    time=forms.CharField(label='Time', max_length=100)
    typ=forms.CharField(label='Type', max_length=100)

    
