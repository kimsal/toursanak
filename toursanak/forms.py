from django import forms
from django.contrib.auth.forms import AuthenticationForm 
class ContactForm(forms.Form):
    contactName = forms.CharField(required=True,max_length=100,label='Name',widget=forms.TextInput(attrs={'placeholder': 'Name','class':'form-control input-lg'}))
    contactEmail = forms.EmailField(required=True,max_length=100,label='Email',widget=forms.TextInput(attrs={'placeholder': 'Email','class':'form-control input-lg'}))
    contactDescription = forms.CharField(max_length=500,required=False,label='Request',widget=forms.Textarea(attrs={'rows':4,'class':'form-control','placeholder': 'Enter Requests here ....'})) 
class BookingForm(forms.Form):
	bookingName = forms.CharField(required=True,max_length=100,label='Name',widget=forms.TextInput(attrs={'placeholder': 'Name...','class':'form-control input-lg'}))
	bookingEmail = forms.EmailField(required=True,max_length=100,label='Email',widget=forms.TextInput(attrs={'placeholder': 'Email...','class':'form-control input-lg'}))
	bookingDescription = forms.CharField(max_length=500,required=False,label='Request',widget=forms.Textarea(attrs={'rows':4,'class':'form-control','placeholder': 'Enter Requests here ....'})) 

#login

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))