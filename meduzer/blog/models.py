from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    DoesNotExist = None
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        verbose_name="Авторство",
        related_name="blog_posts",
        related_query_name="post",
    )
    title = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
        db_index=True,
        help_text=True,
        null=False,
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        allow_unicode=True,
        unique_for_date="publish",
    )
    post_subject = models.CharField(
        max_length=255, blank=False, null=False, db_index=True, default=""
    )
    annotation = models.TextField(max_length=600, blank=True, null=True, db_index=True)
    post_keywords = models.CharField(
        max_length=100, blank=True, null=True, db_index=True
    )
    body = models.TextField(
        blank=True, null=True, db_index=True, verbose_name="Основная часть"
    )
    findings = models.CharField(max_length=600, blank=True, null=True, db_index=True)
    bibliography = models.CharField(
        max_length=600, blank=True, null=True, db_index=True
    )
    # tags = models.ManyToManyField(
    #     "Tag", blank=True, null=True, related_name="posts", verbose_name="Присвойте метки:"
    # )
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("blog:post_detail_url", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("blog:post_update_url", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("blog:post_delete_url", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super(Post, self).save()
        if not self.slug:
            slug = slugify(self.title)
            try:
                post_obj = Post.objects.get(slug=slug)
                slug += "-" + str(self.id)
            except Post.DoesNotExist:
                pass
            self.slug = slug
            self.save()

    class Meta:
        ordering = ("-publish",)
        indexes = [
            GinIndex(fields=["title"], name="gin_trgm_idx", opclasses=["gin_trgm_ops"])
        ]
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return f"{self.title}"


# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name='Комментарии')
#     # name = models.CharField(max_length=80)
# email = models.EmailField()
#     author = models.ForeignKey(User, related_name="comment_author", on_delete=models.CASCADE, verbose_name="Автор")
#     body = models.TextField(verbose_name='Комментарий')
#     created = models.DateTimeField("Опубликовано", auto_now_add=True)
#     updated = models.DateTimeField("Обновлено", auto_now=True)
#     active = models.BooleanField(default=True)
#
#     class Meta:
#         ordering = ("created",)
#         verbose_name='Комментарий'
#         verbose_name_plural="Комментарии"
#
#     def __str__(self):
#         return f"Комментарий от {self.author} к публикации {self.post}"


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название метки")
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name="In english, please"
    )

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
