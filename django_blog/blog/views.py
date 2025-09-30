from django.shortcuts import render
from .models import Post
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm

def post_list(request):
    posts = Post.objects.select_related("author").all()
    return render(request, "blog/post_list.html", {"posts": posts})


def register(request):
    """User sign-up using a small extension of Django's UserCreationForm."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can log in now.")
            return redirect("login")  # name provided in urls
    else:
        form = RegistrationForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile(request):
    """Simple profile editor (first/last name + email)."""
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "blog/profile.html", {"form": form})