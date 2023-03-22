from django.forms import ModelForm
from .models import Income

class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ["income", "expenses"]