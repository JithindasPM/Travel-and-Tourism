from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from frontend.models import state
from frontend.models import destination
from frontend.models import Package

class State_Form(forms.ModelForm):
    class Meta:
        model=state
        fields='__all__'

        widgets = {
            'Name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter State Name'
            }),
            'Image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'Name': 'State Name',
            'Image': 'Upload Image'
        }


class Destination_Form(forms.ModelForm):
    class Meta:
        model=destination
        fields=['State','Name','Image']
        widgets = {
            'State': forms.Select(attrs={'class': 'form-select'}),
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Destination Name'}),
            'Image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'State': 'Select State',
            'Name': 'Destination Name',
            'Image': 'Upload Image',
        }

class Package_Form(forms.ModelForm):
    class Meta:
        model=Package
        fields=['destination','spot','description','duration','amount','Image']

class Admin_Registration_Form(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email'] 

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
