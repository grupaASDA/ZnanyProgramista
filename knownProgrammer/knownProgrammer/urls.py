"""
URL configuration for knownProgrammer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from knownProgrammer.views import (
    homepage,
    login_user,
    logout_user,
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('admin/', admin.site.urls),
    path('programmers/', include('accounts.urls_accounts')),
    path('reset_password/', views.PasswordResetView.as_view(template_name="accounts/reset_password.html"), name="reset_password"),
    path('reset_password_done/', views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_completed/', views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]
