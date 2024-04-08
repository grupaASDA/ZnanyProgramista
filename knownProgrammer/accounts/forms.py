from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm


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


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name']

class PasswordChangedForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label="New password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label="New password confirmation")
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']

class DeleteAccountForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label="Password")

    class Meta:
        model = CustomUser
        fields = ['old_password']

    def __init__(self, *args, **kwargs):
        super(DeleteAccountForm, self).__init__(*args, **kwargs)
        del self.fields['new_password1']
        del self.fields['new_password2']