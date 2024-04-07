from django.contrib.auth import views
from django.urls import path

from accounts.views.function_based_views import (
    login_user,
    logout_user,
    register_user,
    user_update_form,
    password_changed,
    activate,
)
from accounts.views.generic_views import (
    PasswordsChangeView,


)

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('update_user/<int:id>', user_update_form, name="update_user"),
    path('password/', PasswordsChangeView.as_view(template_name='accounts/change_password.html'), name='change_password'),
    path('password_changed/', password_changed ,name="password_changed"),
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
