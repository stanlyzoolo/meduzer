from time import time

from django.utils.text import slugify
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + "-" + str(int(time()))


class Post(models.Model):
    title = models.CharField(
        max_length=500,
        db_index=True,
        verbose_name="Заголовок публикации:",
        help_text="Рекомендуется присваивать краткий и содержательный заголовок, несмотря на сложность используемых терминов.",
    )
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="Автор - это Вы!)",
    )
    body = models.TextField(blank=True, db_index=True, verbose_name="Основная часть")
    tags = models.ManyToManyField(
        "Tag", blank=True, related_name="posts", verbose_name="Присвойте метки:"
    )
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("blog:post_detail_url", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("blog:post_update_url", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("blog:post_delete_url", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title


# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     body = models.TextField(verbose_name='Комментарий')
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)
#
#     class Meta:
#         ordering = ("created",)
#
#     def __str__(self):
#         return "Комментарий от {} к публикации {}".format(self.name, self.post)


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    # Функция используется для получения ссылки (каноническая ссылка - соглашение Джанго) на объект
    def get_absolute_url(self):
        return reverse("blog:tag_detail_url", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("blog:tag_update_url", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("blog:tag_delete_url", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["title"]
