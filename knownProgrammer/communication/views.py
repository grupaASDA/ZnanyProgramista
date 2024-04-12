from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages



from accounts.models import CustomUser
from programmers.models import ProgrammerProfile
from communication.forms import CommunicationCreationModelForm
from communication.models import Communicate


# Create your views here.

@login_required(login_url="/accounts/login/")
def send_message_view(request, id):
    programmer_profile_exists = ProgrammerProfile.objects.filter(user_id=id).exists()
    if not programmer_profile_exists:
        raise PermissionDenied("Programmer not found")
    user_id = request.user.id
    sent_by_user = get_object_or_404(CustomUser, id=user_id)
    sent_to_user = get_object_or_404(CustomUser, id=id)
    form = CommunicationCreationModelForm
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
        form = CommunicationCreationModelForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sent_by = sent_by_user
            message.sent_to = sent_to_user
            message.save()
            messages.success(request, ("Your message has been successfully sent"))
            return redirect("homepage")
        ctx = {
            'sent_by_user': sent_by_user,
            'sent_to_user': sent_to_user,
            'form': form,
            'previous_page': previous_page,
        }
        messages.error(
            request,
            ("Something went wrong")
        )
        return render(request, template_name="communication/send_message.html", context=ctx)

@login_required(login_url="/accounts/login/")
def my_messages_person_list_view(request):
    people_i_sent_message = Communicate.objects.filter(sent_by=request.user.id).values('sent_to').distinct()
    people_who_sent_message = Communicate.objects.filter(sent_to=request.user.id).values('sent_by').distinct()

    people_i_sent_message_info = [get_object_or_404(CustomUser, id=user_id['sent_to']) for user_id in people_i_sent_message]
    people_who_sent_message_info = [get_object_or_404(CustomUser, id=user_id['sent_by']) for user_id in people_who_sent_message]

    if request.method == 'GET':
        ctx = {
            'people_i_sent_message': people_i_sent_message_info,
            'people_who_sent_message': people_who_sent_message_info,
        }
        return render(request, 'communication/my_messages_person_list.html', context=ctx)

@login_required(login_url="/accounts/login/")
def my_messages_with_xyz_view(request, id):
    user_info = get_object_or_404(CustomUser, id=id)
    messages_sent_by_me = Communicate.objects.filter(sent_by=request.user.id, sent_to=id)
    messages_sent_to_me = Communicate.objects.filter(sent_by=id, sent_to=request.user.id)
    if request.method == 'GET':
        ctx = {
            'user_info': user_info,
            'messages_sent_by_me': messages_sent_by_me,
            'messages_sent_to_me': messages_sent_to_me,
        }
        return render(request, 'communication/my_messages_with_xyz.html', context=ctx)

@login_required(login_url="/accounts/login/")
def message_view(request, id):
    message = get_object_or_404(Communicate, id=id)
    previous_page = request.META.get('HTTP_REFERER')
    if message.sent_by != request.user and message.sent_to != request.user:
        raise PermissionDenied("You can't see this message")
    if request.method == 'GET':
        ctx = {
            'message': message,
            'previous_page': previous_page,
        }
        return render(request, 'communication/message.html', context=ctx)










