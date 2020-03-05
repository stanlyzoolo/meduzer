from django import forms
from django.contrib.auth.models import User
from django.db import models
# from meduzer.account.models.place_of_study import PlaceOfStudy
# from meduzer.account.models.place_of_working import PlaceOfWork


class UserBio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_bio = models.ImageField(upload_to="avatars_bio/", null=True, blank=True)
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    # place_of_study = forms.ModelChoiceField(
    #     queryset=PlaceOfStudy.objects.all(),
    #     required=False,
    #     label="Выберите образование",
    # )
    # place_of_work = forms.ModelChoiceField(
    #     queryset=PlaceOfWork.objects.all(), required=False, label="Место работы"
    # )
