from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from taggit.models import Tag

from .forms import PostForm, TagForm
from .models import Post
from .utils import ObjectCreateMixin, ObjectDetailMixin


def posts_list(request):
    search_query = request.GET.get("search", "")

    if search_query:
        posts = Post.objects.filter(
            Q(title_icontains=search_query) | Q(body__icontains=search_query)
        )
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f"?page={page.previous_page_number()}"
    else:
        prev_url = ""

    if page.has_next():
        next_url = f"?page={page.next_page_number()}"
    else:
        next_url = ""

    context = {
        "page_object": page,
        "is_paginated": is_paginated,
        "prev_url": prev_url,
        "next_url": next_url,
    }

    return render(request, "blog/post/list.html", context=context)


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = "blog/post/post_create_form.html"
    raise_exception = True


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = "blog/post/detail.html"


class PostUpdate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = Post
    model_form = PostForm
    template = "blog/post_update_form.html"
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectCreateMixin, View):
    model = Post
    template = "post_delete_form.html"
    redirect_url = "posts_list_url"
    raise_exception = True


# def post_share(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     sent = False
#     if request.method == "POST":
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = '{}({}) рекомендуется для прочтения "{}"'.format(
#                 cd["name"], cd["email"], post.title
#             )
#             message = 'Прочитать "{}" от {}\n\n{}`s comments:{}'.format(
#                 post.title, post_url, cd["name"], cd["comments"]
#             )
#             send_mail(subject, message, "admin@myblog.com", [cd["to"]])
#             sent = True
#     else:
#         form = EmailPostForm()
#     return render(
#         request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
#     )


# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
#     if "query" in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data["query"]
#             results = (
#                 Post.objects.annotate(similarity=TrigramSimilarity("title", query), )
#                     .filter(similarity__gt=0.3)
#                     .order_by("-similarity")
#             )
#     return render(
#         request,
#         "blog/post/search.html",
#         {"form": form, "query": query, "results": results},
#     )


class TagDetail(ObjectCreateMixin, View):
    model = Tag
    template = "blog/tags/tag_detail.html"


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = "blog/tags/tag_create.html"
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = Tag
    model_form = TagForm
    template = "blog/tags/tag_update_form.html"
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectCreateMixin, View):
    model = Tag
    template = "blog/tags/tag_delete_form.html"
    redirect_url = "tags_list_url"
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, "blog/tags/tags_list.html", context={"tags": tags})
