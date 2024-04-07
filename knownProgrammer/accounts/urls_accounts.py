from django.contrib.auth import views
from django.urls import path

from accounts.views import (
    login_user,
    logout_user,
    register_user,
    activate,

)

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('reset_password/', views.PasswordResetView.as_view(template_name="accounts/reset_password.html"),
         name="reset_password"),
    path('reset_password_done/', views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset_password_completed/',
         views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name="password_reset_complete"),
]
