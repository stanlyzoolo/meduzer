from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from .forms import UserRegistrationForm


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": dashboard})


def register(request: HttpRequest):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # создание нового врача
            new_user = user_form.save()
            new_user.refresh_from_db()
            # ub = UserBio(user=new_user, **user_form.cleaned_data)
            # ub.save()
            new_user.UserBio.avatar_bio = user_form.cleaned_data.get("avatar_bio")
            new_user.UserBio.first_name = user_form.cleaned_data.get("first_name")
            new_user.UserBio.last_name = user_form.cleaned_data.get("last_name")
            new_user.UserBio.place_of_study = user_form.cleaned_data("place_of_study")
            new_user.UserBio.place_of_work = user_form.cleaned_data("place_of_work")
            new_user.save()
            username = new_user.cleaned_data["username"]
            password = new_user.cleaned_data["password1"]

            new_user = authenticate(request, username=username, password=password)
            login(request, new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})
