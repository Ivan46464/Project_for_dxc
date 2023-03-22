from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import IncomeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Income


# Create your views here.
login_required(login_url="/login")
def income(response):
    form = IncomeForm()
    if response.method == "POST":
        form = IncomeForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form": form}
    return render(response, "income.html", context)



def home(response):
    return render(response, "home.html", {})

def create(response):

    return
