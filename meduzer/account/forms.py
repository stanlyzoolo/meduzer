from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models.place_of_study import PlaceOfStudy
from .models.place_of_working import PlaceOfWork


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_bio = models.ImageField(upload_to="avatars_bio/", null=True, blank=True)
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    place_of_study = forms.ModelChoiceField(
        queryset=PlaceOfStudy.objects.all(),
        required=False,
        label="Выберите образование",
    )
    place_of_work = forms.ModelChoiceField(
        queryset=PlaceOfWork.objects.all(), required=False, label="Место работы"
    )
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return cd["password2"]
