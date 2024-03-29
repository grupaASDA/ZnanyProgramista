from django.contrib import admin

from .models import CustomUser, ProgrammerProfile

admin.site.register(CustomUser)
admin.site.register(ProgrammerProfile)