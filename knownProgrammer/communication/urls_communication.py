from django.urls import path

from communication.views import (
    send_message_view,
    my_messages_person_list_view,
    my_messages_with_xyz_view,
    message_view,
)

urlpatterns = [
    path('send/<int:id>', send_message_view, name='send_message'),
    path('contacts_list/', my_messages_person_list_view, name='messages_person_list'),
    path('messages_list/<int:id>/', my_messages_with_xyz_view, name='messages_with_list'),
    path('message/<int:id>', message_view, name='message')
]