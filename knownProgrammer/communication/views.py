from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from datetime import datetime

from accounts.models import CustomUser
from communication.forms import MessageCreationModelForm
from communication.models import Message

login_redirect = reverse_lazy("login")

# Create your views here.

def get_last_message(contact, request_user):
    last_message_i_sent_date = Message.objects.filter(sent_by=request_user, sent_to=contact).order_by('created_at').values('created_at').last()
    last_message_i_get_date = Message.objects.filter(sent_to=request_user, sent_by=contact).order_by('created_at').values('created_at').last()
    if last_message_i_sent_date == None:
        return last_message_i_get_date['created_at']
    elif last_message_i_get_date == None:
        return last_message_i_sent_date['created_at']
    else:
        if last_message_i_sent_date['created_at'] > last_message_i_get_date['created_at']:
            return last_message_i_sent_date['created_at']
        else:
            return last_message_i_get_date['created_at']


def get_recipients(recipients_ids:list):
    return {user_id['sent_to']: get_object_or_404(CustomUser, id=user_id['sent_to']) for user_id in recipients_ids}


def get_senders(senders_ids:list):
    return {user_id['sent_by']: get_object_or_404(CustomUser, id=user_id['sent_by']) for user_id in senders_ids}

def delete_contact_duplicates(senders, recipients):
    contacts = []
    for contact in recipients.values():
        contacts.append(contact)

    for contact_id, contact in senders.items():
        if contact_id not in recipients.keys():
            contacts.append(contact)

    return contacts

@login_required(login_url=login_redirect)
def send_message_view(request, id):
    user_profile_exists = CustomUser.objects.filter(id=id).exists()
    if not user_profile_exists:
        raise PermissionDenied("User not found")
    elif request.user.id == id:
        raise PermissionDenied("You can't send message to yourself")
    user_id = request.user.id
    sent_by_user = get_object_or_404(CustomUser, id=user_id)
    sent_to_user = get_object_or_404(CustomUser, id=id)
    form = MessageCreationModelForm
    previous_page = request.META.get('HTTP_REFERER')
    if request.method == "GET":
        ctx = {
            'sent_by_user': sent_by_user,
            'sent_to_user': sent_to_user,
            'form': form,
            'previous_page': previous_page,
        }
        return render(request, template_name="communication/send_message.html", context=ctx)
    if request.method == "POST":
        form = MessageCreationModelForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sent_by = sent_by_user
            message.sent_to = sent_to_user
            message.save()
            messages.success(request, ("Your message has been successfully sent"))
            return redirect('messages_person_list')
        ctx = {
            'sent_by_user': sent_by_user,
            'sent_to_user': sent_to_user,
            'form': form,
            'previous_page': previous_page,
        }
        messages.error(request, ("Something went wrong"))
        return render(request, template_name="communication/send_message.html", context=ctx)

def replay_message_view(request, id):
    previous_message = get_object_or_404(Message, id=id)
    user_profile_exists = CustomUser.objects.filter(id=previous_message.sent_by.id).exists()
    message_exists = Message.objects.filter(id=id).exists()
    if not message_exists:
        raise PermissionDenied("Message not found")
    elif not user_profile_exists:
        raise PermissionDenied("User not found")
    elif request.user.id != previous_message.sent_by.id and request.user.id != previous_message.sent_to.id:
        raise PermissionDenied("You have not permission to replay on this messages")
    user_session_id = request.user.id
    if user_session_id == previous_message.sent_by.id:
        sent_by_user = get_object_or_404(CustomUser, id=user_session_id)
        sent_to_user = get_object_or_404(CustomUser, id=previous_message.sent_to.id)
    else:
        sent_by_user = get_object_or_404(CustomUser, id=user_session_id)
        sent_to_user = get_object_or_404(CustomUser, id=previous_message.sent_by.id)
    form = MessageCreationModelForm
    previous_page = request.META.get('HTTP_REFERER')
    if request.method == "GET":
        ctx = {
            'sent_by_user': sent_by_user,
            'sent_to_user': sent_to_user,
            'form': form,
            'previous_page': previous_page,
            'previous_message': previous_message,
        }
        return render(request, template_name="communication/replay_message.html", context=ctx)
    if request.method == "POST":
        form = MessageCreationModelForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sent_by = sent_by_user
            message.sent_to = sent_to_user
            message.save()
            messages.success(request, ("Your message has been successfully sent"))
            return redirect('messages_person_list')
        ctx = {
            'sent_by_user': sent_by_user,
            'sent_to_user': sent_to_user,
            'form': form,
            'previous_page': previous_page,
            'previous_message': previous_message,
        }
        messages.error(request, ("Something went wrong"))
        return render(request, template_name="communication/replay_message.html", context=ctx)

@login_required(login_url=login_redirect)
def my_messages_people_list_view(request):
    recipients_ids = Message.objects.filter(sent_by=request.user).values('sent_to').distinct()
    senders_ids = Message.objects.filter(sent_to=request.user).values('sent_by').distinct()

    senders = get_senders(senders_ids)
    recipients = get_recipients(recipients_ids)

    contacts = delete_contact_duplicates(senders, recipients)

    contacts_with_date = [[contact, get_last_message(contact, request.user)] for contact in contacts]

    contacts_with_date.sort(key=lambda x: x[1], reverse=True)


    if request.method == 'GET':
        ctx = {
            'contacts': contacts_with_date,
        }
        return render(request, 'communication/my_messages_people_list.html', context=ctx)

@login_required(login_url=login_redirect)
def my_messages_with_correspondent_view(request, id):
    user = get_object_or_404(CustomUser, id=id)
    sent_by_me = Message.objects.filter(sent_by=request.user.id, sent_to=id).order_by('-created_at')
    sent_to_me = Message.objects.filter(sent_by=id, sent_to=request.user.id).order_by('-created_at')

    if request.method == 'GET':
        ctx = {
            'user': user,
            'sent_by_me': sent_by_me,
            'sent_to_me': sent_to_me,
        }
        return render(request, 'communication/my_messages_with_correspondent.html', context=ctx)

@login_required(login_url=login_redirect)
def message_view(request, id):
    message = get_object_or_404(Message, id=id)
    if message.sent_by != request.user and message.sent_to != request.user:
        raise PermissionDenied("You can't see this message")
    if request.method == 'GET':
        ctx = {
            'message': message,
        }
        return render(request, 'communication/message.html', context=ctx)














