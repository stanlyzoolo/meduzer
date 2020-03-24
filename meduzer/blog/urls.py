from django.urls import path

from .views import *

app_name = "blog"

urlpatterns = [
    path("", posts_list, name="posts_list_url"),
    path("post/create/", PostCreate.as_view(), name="post_create_url"),
    path("post/<str:slug>/", PostDetail.as_view(), name="post_detail_url"),
    path("post/<str:slug>/update/", PostUpdate.as_view(), name="post_update_url"),
    path("post/<str:slug>/delete/", PostDelete.as_view(), name="post_delete_url"),
    # path("<int:post_id>/share/", views.post_share, name="post_share"),
    # path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    # path("search/", views.post_search, name="post_search"),
    path("tags/", tags_list, name="tags_list_url"),
    path("tags/create/", TagCreate.as_view(), name="tag_create_url"),
    path("tags/<str:slug>/", TagDetail.as_view(), name="tag_detail_url"),
    path("tags/<str:slug>/update/", TagUpdate.as_view(), name="tag_update_url"),
    path("tags/<str:slug>/delete/", TagDelete.as_view(), name="tag_delete_url"),
]
