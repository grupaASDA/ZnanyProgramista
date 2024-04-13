from django.contrib import admin
from django.urls import path, include

from accounts.views.function_based_views import (
    homepage,
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('programmers/', include('programmers.urls_programmers')),
    path('accounts/', include('accounts.urls_accounts')),
    path('messages/', include('communication.urls_communication'))
]
