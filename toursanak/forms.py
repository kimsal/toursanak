from django import forms

class ContactForm(forms.Form):
    contactName = forms.CharField(required=True,max_length=100,label='Name',widget=forms.TextInput(attrs={'placeholder': 'Name','class':'form-control input-lg'}))
    contactEmail = forms.EmailField(required=True,max_length=100,label='Email',widget=forms.TextInput(attrs={'placeholder': 'Email','class':'form-control input-lg'}))
    contactDescription = forms.CharField(max_length=500,required=False,label='Request',widget=forms.Textarea(attrs={'rows':4,'class':'form-control','placeholder': 'Enter Requests here ....'})) 
class BookingForm(forms.Form):
	bookingName = forms.CharField(required=True,max_length=100,label='Name',widget=forms.TextInput(attrs={'placeholder': 'Name...','class':'form-control input-lg'}))
	bookingEmail = forms.EmailField(required=True,max_length=100,label='Email',widget=forms.TextInput(attrs={'placeholder': 'Email...','class':'form-control input-lg'}))
	bookingDescription = forms.CharField(max_length=500,required=False,label='Request',widget=forms.Textarea(attrs={'rows':4,'class':'form-control','placeholder': 'Enter Requests here ....'})) 