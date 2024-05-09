import cloudinary
import cloudinary.uploader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from accounts.models import CustomUser, DEFAULT_AVATAR
from programmers.filters import ProgrammerFilter
from programmers.forms import ProgrammerCreationModelForm, RatingForm, AvatarUploadForm
from programmers.models import ProgrammerProfile, Rating
from programmers.services.cloudinary import configure_cloudinary, generate_random_string


class ProgrammerListView(ListView):
    creators_ids = [1, 2, 3]
    queryset = ProgrammerProfile.objects.all()
    template_name = 'programmers/programmers_list.html'
    context_object_name = 'programmers'

    def get_queryset(self):
        queryset = ProgrammerFilter(self.request.GET, queryset=self.queryset).qs
        current_user = self.request.user
        queryset = queryset.exclude(id=current_user.id)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['form'] = ProgrammerFilter.form
        context['creators'] = self.creators_ids

        if 'experience' in self.request.GET:
            context['experience'] = self.request.GET['experience']

        if 'programming_languages__contains' in self.request.GET:
            context['programming_languages'] = self.request.GET['programming_languages__contains']

        if 'tech_stack__contains' in self.request.GET:
            context['tech_stack'] = self.request.GET['tech_stack__contains']

        if 'wage_min' in self.request.GET:
            context['wage_min'] = self.request.GET['wage_min']

        if 'wage_max' in self.request.GET:
            context['wage_max'] = self.request.GET['wage_max']

        if 'first_name' in self.request.GET:
            context['first_name'] = self.request.GET['first_name']

        if 'last_name' in self.request.GET:
            context['last_name'] = self.request.GET['last_name']

        for programmer in context['programmers']:
            programmer.count = programmer.ratings_count()

        return context


@login_required(login_url="/accounts/login/")
def programmer_detail(request, id):
    rated = False
    user = request.user
    try:
        programmer = get_object_or_404(ProgrammerProfile, id=id)
        programmer.average_rating = programmer.average_rating()
        users_ratings = Rating.objects.filter(user_id=request.user.id, programmer_id=id).first()
        programmer.count = programmer.ratings_count()
        if users_ratings:
            rated = True
            programmer.count = programmer.ratings_count()
    except ProgrammerProfile.DoesNotExist:
        return HttpResponseNotFound("Page not found")
    if request.user.id == programmer.user_id.id:
        owner = True
    else:
        owner = False

    ctx = {
        "programmer": programmer,
        "user": user,
        "rated": rated,
        "owner": owner,
    }

    return render(
        request,
        template_name="programmers/programmer_detail.html",
        context=ctx,
    )


@login_required(login_url="/accounts/login/")
def programmer_create_form(request):
    user_id = request.user.id
    programmer_profile_exists = ProgrammerProfile.objects.filter(user_id=user_id).exists()
    if programmer_profile_exists:
        return HttpResponseForbidden("You have already created a programmer account")
    form = ProgrammerCreationModelForm(request.POST or None)
    if request.method == 'GET':
        ctx = {
            "form": form,
        }
        return render(
            request,
            template_name='programmers/programmer_create_model_form.html',
            context=ctx,
        )

    elif request.method == 'POST':
        form = ProgrammerCreationModelForm(request.POST)
        if form.is_valid():
            programmer = form.save(commit=False)
            programmer.user_id = request.user
            programmer.save()
            request.user.is_dev = True
            request.user.save()
            messages.success(
                request,
                message=f"Programmer {programmer.user_id.first_name} {programmer.user_id.last_name} has been successfully created",
            )

            return redirect(f'/programmers/myprofile/{user_id}')
        ctx = {
            "form": form,
        }
        messages.error(
            request,
            message="Something went wrong",
        )
        return render(
            request,
            template_name='programmers/programmer_create_model_form.html',
            context=ctx,
        )


@login_required(login_url="/accounts/login/")
def programmer_update_model_form(request, id):
    programmer = get_object_or_404(ProgrammerProfile, id=id)
    user = request.user

    if request.user.id == programmer.user_id.id:
        owner = True
    else:
        owner = False
        raise PermissionDenied("You do not have permission to edit this index.")

    if request.method == "GET":
        form = ProgrammerCreationModelForm(instance=programmer)
        ctx = {
            "form": form,
            "user": user,
            'owner': owner,
            "programmer": programmer,
        }
        return render(
            request,
            template_name="programmers/programmer_update_model_form.html",
            context=ctx,
        )
    if request.method == "POST":
        form = ProgrammerCreationModelForm(request.POST, instance=programmer)

        if form.is_valid():
            form.save()
            ctx = {
                "form": form,
                "user": user,
                'owner': owner,
                "programmer": programmer,
            }
            messages.success(
                request,
                message=f"Programmer {programmer.user_id.first_name} {programmer.user_id.last_name} has been successfully edited",
            )
            return render(
                request,
                template_name="programmers/my_profile.html",
                context=ctx,
            )

        ctx = {
            "form": form,
            "user": user,
            "programmer": programmer,
        }
        messages.error(
            request,
            message="Something went wrong",
        )

        return render(
            request,
            template_name="programmers/programmer_update_model_form.html",
            context=ctx,
        )


@login_required(login_url="/accounts/login/")
def programmer_delete_confirm(request, id):
    programmer = get_object_or_404(ProgrammerProfile, id=id)
    programmer.count = programmer.ratings_count()
    user = request.user

    if request.user.id != programmer.user_id.id:
        raise PermissionDenied("You do not have permission to delete this index.")
    if request.method == "GET":
        ctx = {
            "programmer": programmer,
            "user": user,
        }
        return render(
            request,
            template_name="programmers/programmer_delete_confirm.html",
            context=ctx,
        )

    if request.method == "POST":
        programmer.delete()
        request.user.is_dev = False
        request.user.save()
        messages.success(
            request,
            message=f"Programmer {programmer.user_id.first_name} {programmer.user_id.last_name} has been successfully deleted",
        )

        return redirect("my_profile", id=user.id)


@login_required(login_url="/accounts/login/")
def rate_programmer(request, id):
    programmer = get_object_or_404(ProgrammerProfile, id=id)

    if request.method == "GET":
        user = request.user
        if user.id == programmer.user_id.id:
            raise PermissionDenied("You cannot rate yourself.")
        rating_exists = Rating.objects.filter(programmer=programmer, user=user).first()
        if rating_exists:
            form = RatingForm(initial={'rating': rating_exists.rating})
        else:
            form = RatingForm()
        ctx = {
            "programmer": programmer,
            "form": form,
        }
        return render(
            request,
            template_name='programmers/rate_programmer.html',
            context=ctx,
        )

    if request.method == 'POST':
        form = RatingForm(request.POST)
        user = request.user

        if form.is_valid():
            user_rating = form.cleaned_data['rating']
            rating_exists = Rating.objects.filter(programmer=programmer, user=user).first()
            if rating_exists:
                rating_exists.rating = user_rating
                rating_exists.save()
                messages.success(
                    request,
                    message="Your rating has been updated."
                )
            else:
                new_rating = Rating.objects.create(programmer=programmer, user=user, rating=user_rating)
                new_rating.save()
                messages.success(
                    request,
                    message="Your rating has been submitted.",
                )

            rated = False
            try:
                programmer = get_object_or_404(ProgrammerProfile, id=id)
                programmer.average_rating = programmer.average_rating()
                programmer.count = programmer.ratings_count()
                users_ratings = Rating.objects.filter(user_id=user.id, programmer_id=id).first()
                if users_ratings:
                    rated = True
            except ProgrammerProfile.DoesNotExist:
                return HttpResponseNotFound("Page not found")

            ctx = {
                "form": form,
                "programmer": programmer,
                "user": user,
                "rated": rated,
            }

            return render(
                request,
                template_name="programmers/programmer_detail.html",
                context=ctx,
            )

        else:
            messages.error(
                request,
                message="Invalid form submission."
            )
            return redirect('programmers/programmers_list')


@login_required(login_url="/accounts/login/")
def upload_avatar(request, id):
    logged_user = request.user
    user = get_object_or_404(CustomUser, id=id)

    if logged_user.id != user.id:
        raise PermissionDenied("You do not have permission to upload/ update this avatar.")

    if request.method == "GET":
        form = AvatarUploadForm()
        ctx = {
            "form": form,
            "user": user
        }
        return render(
            request,
            template_name='programmers/programmer_avatar_update.html',
            context=ctx,
        )

    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)

        if form.is_valid():
            configure_cloudinary()
            random_str = generate_random_string()
            picture_name = f"{request.FILES['avatar'].name}_{random_str}"
            uploaded_file = request.FILES['avatar']
            r = cloudinary.uploader.upload(uploaded_file, public_id=f'avatars/{picture_name}', overwrite=True)
            version = r.get('version')
            if version:
                src_url = cloudinary.CloudinaryImage(f'avatars/{picture_name}') \
                    .build_url(
                    transformation=[
                        {'gravity': "face", 'height': 200, 'width': 200, 'crop': "thumb"},
                        {'radius': "max"},
                        {'fetch_format': "auto"}
                    ],
                    version=version
                )
                user.avatar = src_url
                user.save()
                messages.success(
                    request,
                    message="Your avatar has been successfully uploaded."
                )
                return redirect('my_profile', id=id)

        else:
            messages.error(
                request,
                message="Invalid form submission."
            )

        ctx = {
            "form": form,
            "user": user,
        }

        return render(
            request,
            template_name="programmers/programmer_avatar_update.html",
            context=ctx,
        )


@login_required(login_url="/accounts/login/")
def restore_avatar(request, id):
    logged_user = request.user
    user = get_object_or_404(CustomUser, id=id)

    if logged_user.id != user.id:
        raise PermissionDenied("You do not have permission to upload/ update this avatar.")

    if request.method == 'POST':
        user.avatar = DEFAULT_AVATAR
        user.save()
        messages.success(
            request,
            message="Your avatar has been successfully restored to default."
        )
        return redirect('my_profile', id=id)

    form = AvatarUploadForm()
    ctx = {
        "form": form,
        "user": user
    }

    return render(
        request,
        template_name="programmers/programmer_avatar_update.html",
        context=ctx,
    )


@login_required(login_url="/accounts/login/")
def my_profile_view(request, id):
    if request.user.id != id:
        raise PermissionDenied("You do not have permission to see someone profile.")
    user = get_object_or_404(CustomUser, id=request.user.id)
    if request.method == "GET":
        if user.is_dev == False:
            ctx = {
                'user': user
            }
            return render(request, "programmers/my_profile.html", context=ctx)
        else:
            programmer = ProgrammerProfile.get_profile_by_user_id(user.id)
            ctx = {
                'user': user,
                'programmer': programmer,
            }
            return render(request, "programmers/my_profile.html", context=ctx)
