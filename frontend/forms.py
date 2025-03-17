from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# class RegistrationForm(UserCreationForm):
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1"]

#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control '}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),

#         }

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm your password"})
    # )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

class LoginForm(forms.Form):
   username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
   password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))