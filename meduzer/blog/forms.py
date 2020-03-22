from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Post, Tag


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")


class SearchForm(forms.Form):
    query = forms.CharField()


class TagForm(forms.Form):
    class Meta:
        model = Tag
        fields = ["title", "slug"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data["slug"].lower()

        if new_slug == "create":
            raise ValidationError("Slug не может быть создан")
        if Tag.objects.filter(slug_iexact=new_slug).count():
            raise ValidationError(
                f"Slug должен быть уникальным. {new_slug} уже существует."
            )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["author"]
        fields = ["title", "slug", "body", "tags"]

        widgets = {
            "title": forms.TextInput(),
            "slug": forms.TextInput(),
            "body": forms.Textarea(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data["slug"].lower()

        if new_slug == "create":
            raise ValidationError("Слаг не может быть создан")
        return new_slug
