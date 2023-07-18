
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("profile/<int:id>/", views.profile, name='profile'),
    path("updatePost", views.updatePost, name='updatePost'),
    path("following", views.following, name="following"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("removePostLike", views.removePostLike, name="removePostLike"),
    path("addPostLike", views.addPostLike, name="addPostLike"),
]
