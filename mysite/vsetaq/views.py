from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item

# Create your views here.
def index(response):

    return



def home(response):
    return render(response, "home.html", {})

def create(response):

    return
