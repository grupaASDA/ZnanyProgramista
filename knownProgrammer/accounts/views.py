from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib import messages

from accounts.forms import ProgrammerCreationModelForm
from accounts.models import ProgramerProfile


def programmers_list(request):
    programmers = ProgramerProfile.objects.all()
    ctx = {
        "programmers": programmers,
    }

    return render(request, template_name="accounts/programmers_list.html", context=ctx)


def programmer_detail(request, id):
    try:
        programmer = ProgramerProfile.objects.get(id=id)
    except ProgramerProfile.DoesNotExist:
        return HttpResponseNotFound("Page not found")

    ctx = {
        "programmer": programmer,
    }

    return render(request, template_name="accounts/programmer_detail.html", context=ctx)


def programmer_create_form(request):
    form = ProgrammerCreationModelForm(request.POST or None)
    if request.method == 'GET':
        ctx = {
            "form": form,
        }
        return render(request, template_name='accounts/programmer_create_model_form.html', context=ctx)

    elif request.method == 'POST':
        form = ProgrammerCreationModelForm(request.POST)
        if form.is_valid():
            programmer = form.save(commit=False)
            programmer.user_id = request.user
            programmer.save()
            return redirect(f'/programmers/detail/{programmer.id}')
        ctx = {
            "form": form,
            "error": "Something went wrong",
        }
        return render(request, template_name='accounts/programmer_create_model_form.html', context=ctx)


def programmer_update_model_form(request, id):
    programmer = get_object_or_404(ProgramerProfile, id=id)
    if request.user_id.id != programmer.user_id.id:
        raise PermissionDenied("You do not have permission to edit this index.")

    if request.method == "GET":
        form = ProgrammerCreationModelForm(instance=programmer)
        ctx = {
            "form": form,
            "programmer": programmer,
        }
        return render(
            request, "accounts/programmer_update_model_form.html", context=ctx
        )
    if request.method == "POST":
        form = ProgrammerCreationModelForm(request.POST, instance=programmer)

        if form.is_valid():
            form.save()
            ctx = {
                "form": form,
                "programmer": programmer,
                "message": f"Programmer with id: {id} has been successfully updated",
            }
            return render(
                request, "accounts/programmer_update_model_form.html", context=ctx
            )

        ctx = {
            "form": form,
            "programmer": programmer,
            "message": "Something went wrong",
        }
        return render(
            request, "accounts/programmer_update_model_form.html", context=ctx
        )


def programmer_delete_confirm(request, id):
    programmer = get_object_or_404(ProgramerProfile, id=id)
    if request.user_id.id != programmer.user_id.id:
        raise PermissionDenied("You do not have permission to delete this index.")
    if request.method == "GET":
        ctx = {
            "programmer": programmer,
        }
        return render(request, "accounts/programmer_delete_confirm.html", context=ctx)

    if request.method == "POST":
        programmer.delete()
        messages.success(
            request, f"Programmer with id: {id} has been successfully deleted"
        )

        return redirect("programmers_list")
