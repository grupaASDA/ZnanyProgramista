from django.contrib import admin

from .models import CustomUser, ProgramerProfile

admin.site.register(CustomUser)
admin.site.register(ProgramerProfile)