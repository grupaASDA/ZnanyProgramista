from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm


def homepage(request):
    return render(request, template_name='accounts/home_page.html')


def login_user(request):
    if request.method == "POST":
        user_email = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(request, email=user_email, password=user_password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Logged in succesfully!"))
            return redirect("homepage")
        else:
            messages.error(request, ("Invalid Email or Password!"))
            return redirect("login")

    if request.method == "GET":
        return render(request, template_name='accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect("homepage")

def register_user(request):
    if request.method == "GET":
        form = SignUpForm
        ctx = {
            'form':form,
        }
        return render(request, 'accounts/register_user.html', context=ctx)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, ("Registration successful"))
            return redirect("homepage")
        else:
            messages.error(request, ("Registration failed"))
            ctx = {
                'form' : form,
            }
            return render(request, 'accounts/register_user.html', context=ctx)
