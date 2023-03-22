from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.contrib.auth import authenticate, login

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    income = models.CharField(max_length=120)
    expenses = models.CharField(max_length=120)
    updated = models.DateTimeField(auto_now=True)


