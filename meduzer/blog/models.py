from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField("Tag", blank=True, related_name="posts")
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("blog:post_detail_url", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("post_update_url", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("post_delete_url", kwargs={"slug": self.slug})

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "Комментарий от {} к публикации {}".format(self.name, self.post)


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("tag_detail_url", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("tag_update_url", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("tag_delete_url", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["title"]
