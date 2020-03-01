from django.contrib.auth.models import UserManager
from django.db import models


class PlaceOfWork(models.Model):
    objects = UserManager()
    work = models.TextField(unique=True)

    class Meta:
        verbose_name_plural = "place_of_work"
        ordering = ["work"]

        def __init__(self):
            self.work = self.work

        def __str__(self):
            return f"{self.work}"
