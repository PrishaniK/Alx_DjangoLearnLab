from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to show library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Registration view
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('list_books')
        return render(request, 'relationship_app/register.html', {'form': form})

# Login view using Django's built-in view
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# Logout view using Django's built-in view
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'