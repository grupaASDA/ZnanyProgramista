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
    # Query ORM Djangowego, aby wyciągnąć konkrenty element z tabeli. Jeśli nie będzie żadnego
    # wyniku lub więcej niż jeden, to zostanie wyrzucony błąd.
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
            programmer = form.save()
            return redirect(f'/programmers/detail/{programmer.id}')
        ctx = {
            "form": form,
            "error": "Something went wrong",
        }
        return render(request, template_name='accounts/programmer_create_model_form.html', context=ctx)
