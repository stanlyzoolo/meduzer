from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
    CreateView,
    FormView,
    DeleteView,
)
from django.views.generic.base import View

from .forms import PostForm, TagForm, SearchForm
from .models import Post, Tag
from .postforms.postforms import FullPostForm
from .utils import (
    ObjectCreateMixin,
    ObjectUpdateMixin,
    ObjectDeleteMixin,
    timezone,
)


class PostCreate(LoginRequiredMixin, CreateView, FormView):
    model = Post
    form_class = FullPostForm
    template_name = "blog/post/post_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        from django.http import HttpResponseRedirect

        return HttpResponseRedirect(self.get_success_url())


class PostDetail(DetailView):
    model = Post
    template_name = "blog/post/post_detail.html"
    redirect_url = reverse_lazy("blog:post_detail_url")

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context["now"] = timezone.now()
        return context


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = "blog/post/post_list.html"


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post/post_update_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post/post_delete_form.html"
    success_url = reverse_lazy("blog:posts_list_url")

    def test_func(self):
        return self.get_object().author == self.request.user


class TagDetail(DetailView):
    model = Tag
    template_name = "blog/tags/tag_detail.html"


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = "blog/tags/tag_create.html"
    raise_exception = True


class TagUpdate(LoginRequiredMixin, UserPassesTestMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = "blog/tags/tag_update_form.html"
    raise_exception = True


class TagDelete(LoginRequiredMixin, UserPassesTestMixin, ObjectDeleteMixin, View):
    model = Tag
    template = "blog/tags/tag_delete_form.html"
    redirect_url = reverse_lazy("tags_list_url")
    raise_exception = True


class TagsView(ListView):
    model = Tag
    template_name = "blog/tags/tags_list.html"


class SearchResultsView(ListView):
    model = Post
    template_name = "blog/post/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.objects.filter(
            Q(title__icontains=query)
            | Q(body__icontains=query)
            | Q(post_keywords__icontains=query)
        )
        return object_list
