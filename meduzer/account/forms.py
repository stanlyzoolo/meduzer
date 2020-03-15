from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm

from .models.place_of_study import PlaceOfStudy
from .models.place_of_working import PlaceOfWork

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    avatar_bio = forms.ImageField(label="Аватар")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    birth_date = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={"type": "date"}))
    place_of_study = forms.ModelChoiceField(
        queryset=PlaceOfStudy.objects.all(),
        required=False,
        label="Выберите образование",
    )
    place_of_work = forms.ModelChoiceField(
        queryset=PlaceOfWork.objects.all(), required=False, label="Место работы"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "avatar_bio",
            "first_name",
            "last_name",
            "birth_date",
            "place_of_study",
            "place_of_work")
