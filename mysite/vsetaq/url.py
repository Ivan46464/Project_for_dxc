from django.urls import path, include
from . import views


urlpatterns = [
    path("income/", views.income, name="income"),
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
]