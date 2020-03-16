from django import forms
from django.contrib.auth.models import User
from django.db import models

# from django.db.models.signals import post_save
# from django.dispatch import receiver
from meduzer.account.models.place_of_study import PlaceOfStudy
from meduzer.account.models.place_of_working import PlaceOfWork


class UserBio(models.Model):
    new_user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_bio = models.ImageField(upload_to="avatars_bio/", null=True, blank=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    place_of_study = forms.ModelChoiceField(
        queryset=PlaceOfStudy.objects.all(),
        required=False,
        label="Выберите образование",
        null=True,
    )
    place_of_work = forms.ModelChoiceField(
        queryset=PlaceOfWork.objects.all(),
        required=False,
        label="Место работы",
        null=True,
    )


#
# # метод, который создает User, если создан объект UserBio
# @receiver(post_save, sender=User)
# def new_user(sender, instance, created, **kwargs):
#     if created:
#         UserBio.objects.create(user=instance)
#         instance.UserBio.save()
