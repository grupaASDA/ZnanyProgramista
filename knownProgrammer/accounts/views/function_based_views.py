from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from accounts.models import CustomUser
from accounts.tokens import account_activation_token
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
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import SignUpForm, UserUpdateForm
from accounts.models import CustomUser
from accounts.tokens import change_email_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


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

def password_changed(request):
    return render(request, 'accounts/changed_password.html')

def change_old_email(request, uidb64, token):
    User = CustomUser
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and change_email_token.check_token(user, token):
        changeNewEmail(request, user, user.new_email)
        messages.success(request, (f"Dear {user.first_name} Go to your {user.new_email} box to end changing your email address"))
    else:
        messages.error(request, "Email changing link is invalid")
    return redirect("homepage")
def change_new_email(request, uidb64, token):
    User = CustomUser
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and change_email_token.check_token(user, token):
        user.email = user.new_email
        user.new_email = ""
        user.save()
        messages.success(request, ("Email successfully changed"))
    else:
        messages.error(request, "Email changing link is invalid")
    return redirect("homepage")

def changeOldEmail(request, user, to_email):
    mail_subject = "Change your email address"
    message = render_to_string(
        "accounts/change_old_email_message.html",
        {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': change_email_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear {user.first_name}, please go to your email {to_email} inbox and click on received link to confirm and go to the next step in changing your email. Check your spam folder.")
    else:
        messages.error(request, f"There is problem sending email to {to_email}. Check if you typed the email correctly")

def changeNewEmail(request, user, to_email):
    mail_subject = "Change your email address"
    message = render_to_string(
        "accounts/change_new_email_message.html",
        {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': change_email_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        pass
    else:
        messages.error(request, f"There is problem sending email to {to_email}. Check if you typed the email correctly")
@login_required(login_url='/login/')
def user_update_form(request, id):
    if request.user.id != id:
        raise PermissionDenied("You can't update someone's profile")
    old_user = get_object_or_404(CustomUser, id=id)
    old_email = old_user.email
    if request.method == "GET":
        form = UserUpdateForm(instance=old_user)
        ctx = {
            'form': form,
            'user': old_user,
        }
        return render(request, "accounts/user_update_form.html", context=ctx)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=old_user)

        if form.is_valid():
            new_user = form.save(commit=False)
            if new_user.email == old_email:
                new_user.save()
                messages.success(request, ("Data has been changed"))
                return redirect("homepage")
            new_user.new_email = new_user.email
            new_user.email = old_email
            new_user.save()
            changeOldEmail(request, new_user, new_user.email)
            return redirect("homepage")
        else:
            messages.error(request, ("User profile update failed"))
            ctx = {
                'form': form,
            }
            return render(request, 'accounts/user_update_form.html', context=ctx)





