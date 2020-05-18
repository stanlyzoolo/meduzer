from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from pagedown.widgets import PagedownWidget

from .models import Post, Tag


# class EmailPostForm(forms.Form):
#     name = forms.CharField(max_length=25)
#     email = forms.EmailField()
#     to = forms.EmailField()
#     comments = forms.CharField(required=False, widget=forms.Textarea)

#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ("body",)
#
#     def save(self, commit=True):
#         comment = super(CommentForm, self).save(commit=False)
#         comment.content = self.cleaned_data['body']
#
#         if commit:
#             comment.save()
#         return comment


class SearchForm(forms.Form):
    query = forms.CharField(max_length=150)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["title", "slug"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_slug(self):
        # import pudb;pu.db
        new_slug = self.cleaned_data["slug"].lower()

        if new_slug == "create":
            raise ValidationError("Slug не может быть создан")
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(
                f"Slug должен быть уникальным. {new_slug} уже существует."
            )
        return new_slug


class PostForm(forms.ModelForm):

    body = forms.CharField(
        widget=PagedownWidget(),
        label="Содержание публикации",
        help_text="Воспользуйтесь панелью редактирования для работы с текстом",
    )
    bibliography = forms.CharField(
        widget=PagedownWidget(), label="Поделитесь полезными источниками"
    )
    findings = forms.CharField(
        widget=PagedownWidget(),
        label="В заключении подведите итог и сформулируйте выводы",
    )

    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["publish", "updated", "author", "slug"]
        # разобраться с автозаполнением даты публикации (необязательно, но попробовать)
        widgets = {
            # "author": forms.TextInput(attrs={"author": "user.first_name"}) ,
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "post_subject": forms.TextInput(attrs={"class": "form-control"}),
            "annotation": forms.TextInput(attrs={"class": "form-control"}),
            "post_keywords": forms.TextInput(attrs={"class": "form-control"}),
            "findings": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            # 'publish': forms.DateTimeField(widget=DateTimeInput())
        }

        labels = {
            "title": _("Заголовок публикации"),
            "slug": _("Слаг публикации"),
            "post_subject": _("Предмет публикации (необязательное поле)"),
            "annotation": _("Аннотация (необязательное поле)"),
            "post_keywords": _("Ключевые слова (необязательное поле)"),
            "body": _("Основная часть"),
            "findings": _("Выводы (необязательное поле)"),
            "bibliography": _("Источники и полезные ресурсы (необязательное поле)"),
        }

        help_texts = {
            "title": _("Используйте простые конструкции для оформления заголовка"),
            "post_subject": _("Кратко опишите предмет изучения, либо исследования"),
            "annotation": _(
                "Составьте краткий анонс Вашей публикации: назначение, методы работы, особое внимание к "
                "деталям и отличительные особенности"
            ),
            "post_keywords": _(
                "Используйте ключевые для обнаружения вашей публикации поисковыми сервисами"
            ),
            "findings": _(
                "Подведите итоги Вашей работы для лучшего восприятия читателями ресурса"
            ),
            "tags": _("Присвоение тегов облегчит поиск информации на Medbrain"),
        }

        error_messages = {
            "Post._meta.get_fields()": {
                "max_length": _("Количество символов превышает допустимое"),
            }
        }
