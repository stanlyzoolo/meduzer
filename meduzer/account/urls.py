from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html")),
    path("logout/", auth_views.LogoutView.as_view(template_name="account/logout.html")),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("", include("django.contrib.auth.urls")),
    path("edit/", views.edit, name="edit"),
]
