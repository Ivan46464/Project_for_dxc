from django.db import models

class ToDoList(models.Model):
    income = models.CharField(max_length=120)
    expenses = models.CharField(max_length=120)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text
