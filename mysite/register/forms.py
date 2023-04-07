from typing import Type

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'