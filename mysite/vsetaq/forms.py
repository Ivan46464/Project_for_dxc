from django.forms import ModelForm
from django import forms
from .models import Income, Expenses, Goals


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'income': forms.TextInput(attrs={'class': 'form-control'})
        }


class ExpensesForm(ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'expenses': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.TextInput(attrs={'class': 'form-control'})

        }


class GoalsForm(ModelForm):

    class Meta:
        model = Goals
        fields = '__all__'
        exclude = ['user', 'finished']
        widgets = {
            'save_money': forms.TextInput(attrs={'class': 'form-control'}),
            'goal': forms.TextInput(attrs={'class': 'form-control'})
        }