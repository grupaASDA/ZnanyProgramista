from django.urls import path

from accounts.views import (
    programmer_detail,
    programmers_list,
    programmer_create_form,

)

urlpatterns = [
    path('list', programmers_list, name="programmers_list"),
    path('detail/<int:id>', programmer_detail, name="programmer_detail"),
    path('create', programmer_create_form, name="programmer_create_form"),
]