from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import CustomUser
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

def activate(request, uidb64, token):
    User = CustomUser
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, ("Registration successful"))
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid")
    return redirect("homepage")

def activeEmail(request, user, to_email):
    mail_subject = "Active your user account."
    message = render_to_string(
        "accounts/template_activate_account.html",
        {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear {user.first_name}, please go to your email {to_email} inbox and click on received activation link to confirm and complete te registration. Check your spam folder.")
    else:
        messages.error(request, f"There is problem sending email to {to_email}. Check if you typed the email correctly")


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
            'form': form,
        }
        return render(request, 'accounts/register_user.html', context=ctx)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activeEmail(request, user, form.cleaned_data.get('email'))
            return redirect("homepage")
        else:
            messages.error(request, ("Registration failed"))
            ctx = {
                'form' : form,
            }
            return render(request, 'accounts/register_user.html', context=ctx)
