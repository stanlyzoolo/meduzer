from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _

from django.db import models
from .models.place_of_study import PlaceOfStudy
from .models.place_of_working import PlaceOfWork
from .models.userbio import UserBio

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserBio
        fields = UserCreationForm.Meta.fields + (
            "avatar_bio",
            "first_name",
            "last_name",
            "birth_date",
        )
