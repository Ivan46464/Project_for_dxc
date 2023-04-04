from django.contrib import admin
from .models import Income, Expenses, Goals
# Register your models here.
admin.site.register(Income)
admin.site.register(Expenses)
admin.site.register(Goals)