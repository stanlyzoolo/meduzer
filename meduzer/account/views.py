from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, LoginForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("blog:list", request)
                else:
                    return HttpResponse("Несуществующая учетная запись")
            else:
                return HttpResponse("Неверный логин")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request: HttpRequest):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # создание нового врача
            new_user = user_form.save()
            new_user.save()
            Profile.objects.create(user=new_user)
            username = user_form.cleaned_data["username"]
            password = user_form.cleaned_data["password1"]
            new_user = authenticate(request, username=username, password=password)
            login(request, new_user)
            return render(request, "account/dashboard.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль успешно обновлён")
        else:
            messages.error(request, "Ошибка при обновлении профиля")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


# class RegistrationModel()
# обернуть вьюхи в классы
