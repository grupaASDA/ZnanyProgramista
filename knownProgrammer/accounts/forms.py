from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(),
        strip=False,
    )
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
        ]