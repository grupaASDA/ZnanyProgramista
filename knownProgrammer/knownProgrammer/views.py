from django.shortcuts import render


def homepage(request):
    return render(request, template_name="accounts/home_page.html")
