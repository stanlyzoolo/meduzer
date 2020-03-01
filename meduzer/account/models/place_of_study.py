from django.contrib.auth.models import UserManager
from django.db import models


class PlaceOfStudy(models.Model):
    objects = UserManager()
    place = models.TextField(unique=True)

    class Meta:
        verbose_name_plural = "place_of_study"
        ordering = ["place"]

        def __init__(self):
            self.place = self.place

        def __str__(self):
            return f"{self.place}"
