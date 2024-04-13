from django.urls import path

from programmers.views import (
    programmer_detail,
    ProgrammerListView,
    programmer_create_form,
    programmer_update_model_form,
    programmer_delete_confirm,
    rate_programmer,
    upload_avatar,
    restore_avatar,
    my_profile_view,
)

urlpatterns = [
    path('list', ProgrammerListView.as_view(), name="programmers_list"),
    path('detail/<int:id>', programmer_detail, name="programmer_detail"),
    path('create', programmer_create_form, name="programmer_create_form"),
    path('update/<int:id>', programmer_update_model_form, name="programmer_update_model_form"),
    path('delete/<int:id>', programmer_delete_confirm, name="programmer_delete_confirm"),
    path('rate/<int:id>/', rate_programmer, name='rate_programmer'),
    path('avatar/<int:id>/', upload_avatar, name='upload_avatar'),
    path('restore_avatar/<int:id>/', restore_avatar, name='restore_avatar'),
    path('myprofile/<int:id>', my_profile_view, name='my_profile')
]
