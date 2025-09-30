from django.urls import path
from django.contrib.auth import views as auth_views
from .views import post_list, register, profile
from .views import (
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    register, profile,
)

urlpatterns = [
    
    path("posts/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-edit"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    
    path("post/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment-create-alt"),
    
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update-alt"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete-alt"),
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment-create-postpk-alt"),
    
    path("", PostListView.as_view(), name="post-list"),
    path("", post_list, name="post-list"),
    
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    
    path("post/new/", PostCreateView.as_view(), name="post-create-alt"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update-alt"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete-alt"),
    
    
    
    path("login/",  auth_views.LoginView.as_view(template_name="blog/login.html"),  name="login"),
    path("logout/", auth_views.LogoutView.as_view(),                                name="logout"),
    path("register/", register,                                                     name="register"),
    path("profile/",  profile,                                                      name="profile"),
    
    
]
