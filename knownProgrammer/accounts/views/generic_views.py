from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from accounts.forms import PasswordChangedForm


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangedForm
    success_url = reverse_lazy('password_changed')