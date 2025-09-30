from django.urls import path
from django.contrib.auth import views as auth_views
from .views import post_list, register, profile

urlpatterns = [
    path("", post_list, name="post-list"),
    
    path("login/",  auth_views.LoginView.as_view(template_name="blog/login.html"),  name="login"),
    path("logout/", auth_views.LogoutView.as_view(),                                name="logout"),
    path("register/", register,                                                     name="register"),
    path("profile/",  profile,                                                      name="profile"),
]
