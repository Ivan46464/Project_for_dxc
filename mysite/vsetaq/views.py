from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import IncomeForm, ExpensesForm, GoalsForm
from .models import Expenses
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Income, Goals
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import math

# Create your views here.


def income(response):
    income = Income.objects.filter(user=response.user)

    # income = get_object_or_404(Income, user=response.user)
    form = IncomeForm()
    if response.method == "POST":
        form = IncomeForm(response.POST)
        if form.is_valid():
            income1 = form.save(commit=False)
            income1.user = response.user
            income1.save()
            return redirect('/')
    context = {
        "form": form,
        'income_exists': True if income else False
    }
    return render(response, "income.html", context)


def home(response):
    return render(response, "home.html", {})


def expenses(response):
    form = ExpensesForm()
    if response.method == "POST":
        form = ExpensesForm(response.POST)
        if form.is_valid():
            expenses1 = form.save(commit=False)
            expenses1.user = response.user
            expenses1.save()
            form.save()
            return redirect('/')
    context = {"form": form}
    return render(response, "expenses.html", context)


def chart(response):
    host = response.user
    qs = Expenses.objects.filter(user=host)

    data = [
        {
            'expenses': x.expenses,
            'categories': x.categories,

        }
        for x in qs
    ]
    df = pd.DataFrame(data)
    fig = px.bar(df, y='expenses', color='categories', x='categories')
    # fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type="div")
    context = {'plot_div': gantt_plot}
    return render(response, 'chart.html', context)


def pie_chart(response):
    host = response.user
    qs = Expenses.objects.filter(user=host)
    data = [
        {
            'expenses': x.expenses,
            'categories': x.categories,

        }
        for x in qs
    ]
    df = pd.DataFrame(data)
    fig = px.pie(df, values='expenses', names='categories', color='categories')
    # fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type="div")
    context = {'plot_div': gantt_plot}
    return render(response, 'pie_chart.html', context)


def edit_income(response):
    income = Income.objects.get(user=response.user)
    form = IncomeForm(instance=income)
    if response.method == 'POST':
        form = IncomeForm(response.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(response, "income.html", context)


def goal(response):
    income = Income.objects.get(user=response.user)
    year_income = income.income * 12
    expenses = Expenses.objects.filter(user=response.user)
    all_expenses = 0
    for expense in expenses:
        all_expenses += expense.expenses
    success = income.income - all_expenses
    form = GoalsForm()
    if response.method == "POST":
        form = GoalsForm(response.POST)
        if form.is_valid():
            goals1 = form.save(commit=False)
            goals1.user = response.user
            goals1.save()
            form.save()
    if form.is_valid():
        goals1 = form.save(commit=False)
        goals1.user = response.user
        goals1.save()
        wanted_money = form.cleaned_data.get('save_money', 0)
    else:
        wanted_money = 0
    check_goals1 = Goals.objects.filter(user=response.user).latest('id')
    how_many = math.ceil(wanted_money/success)
    context = {
        "form": form,
        "income": income,
        "amount": year_income,
        "expenses": all_expenses,
        "check_goals": check_goals1,
        "wanted_money": wanted_money,
        "how_many": how_many,
        "success": success
    }
    return render(response, "goals.html", context)


def check_goals(response):
    check_goals1 = Goals.objects.filter(user=response.user)
    context = {
        'check_goals': check_goals1
    }
    return render(response, "check_goals.html", context)


def goal_detail(request, goal_id):
    goal = Goals.objects.get(id=goal_id)
    income = Income.objects.get(user=request.user)
    year_income = income.income * 12
    expenses = Expenses.objects.filter(user=request.user)
    all_expenses = 0
    for expense in expenses:
        all_expenses += expense.expenses
    success = income.income - all_expenses
    wanted_money = goal.save_money
    how_many = wanted_money / success

    context = {
        "goal": goal,
        "income": income,
        "amount": year_income,
        "expenses": all_expenses,
        "wanted_money": wanted_money,
        "how_many": how_many,
        "success": success,
    }
    return render(request, 'goal_detail.html', context)


def delete_goal(response, goal_id):
    goal = get_object_or_404(Goals, id=goal_id)
    if response.method == 'POST':
        goal.delete()
        return redirect('/check_goals')
    else:
        return redirect('/goal_detail', goal_id=goal.id)


def edit_goal(response, goal_id):
    goal = get_object_or_404(Goals, id=goal_id)
    form = GoalsForm(instance=goal)
    if response.method == 'POST':
        form = GoalsForm(response.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('/check_goals')
    context = {'form': form}
    return render(response, "goals.html", context)


def check_expenses(response):
    expenses = Expenses.objects.filter(user=response.user)
    context = {
        "expenses": expenses
    }
    return render(response, "check_expenses.html", context)


def expenses_detail(response, expense_id):
    expenses = Expenses.objects.get(user=response.user, id=expense_id)
    context = {
        "expenses": expenses
    }
    return render(response, 'expenses_detail.html', context)


def delete_expense(response, expense_id):
    expenses = get_object_or_404(Expenses, id=expense_id)
    if response.method == 'POST':
        expenses.delete()
        return redirect('/check_expenses')
    else:
        return redirect('/expenses_detail', goal_id=expenses.id)


def edit_expenses(response, expense_id):
    expenses = get_object_or_404(Expenses, id=expense_id)
    form = ExpensesForm(instance=expenses)
    if response.method == 'POST':
        form = ExpensesForm(response.POST, instance=expenses)
        if form.is_valid():
            form.save()
            return redirect('/check_expenses')
    context = {'form': form}
    return render(response, "expenses.html", context)


def user_profile(response):
    host = response.user
    income = Income.objects.get(user=host)
    amount = income.income
    context = {
        "amount": amount
    }
    return render(response, "user_profile.html", context)