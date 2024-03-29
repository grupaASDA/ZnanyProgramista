from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login


def homepage(request):
    return render(request, template_name="accounts/home_page.html")

def login_user(request):
    if request.method == "POST":
        user_email = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(request, email=user_email, password=user_password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have logged in successfully!"))
            return redirect("homepage")
        else:
            messages.error(request, ("Invalid Email or Password!"))
            return redirect("login")


    if request.method == "GET":
        return render(request, template_name='accounts/login.html')
