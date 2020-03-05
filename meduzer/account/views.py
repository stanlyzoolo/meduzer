from django.http import HttpResponse, request, HttpRequest
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models.userbio import UserBio


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": dashboard})


def register(request: HttpRequest):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # создание нового врача
            new_user = user_form.save(commit=False)
            # присвоение зашифрованного пароля пользователю
            new_user.set_password(user_form.cleaned_data["password"])
            # сэйв в базе
            new_user.save()

            bio = UserBio(user=new_user, )
            bio.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})
