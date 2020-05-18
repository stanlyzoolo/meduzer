from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar_bio = models.ImageField(upload_to="users/%Y/%m/%d/", null=True, blank=False)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Профиль пользователя {self.user}"
