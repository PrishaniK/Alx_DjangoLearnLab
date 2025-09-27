from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, BookViewSet,
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")

urlpatterns = [
    # Router endpoints (ViewSets)
    path("", include(router.urls)),

    # Generic views (single, clean set)
    path("books/", ListView.as_view(), name="book-list"),
    path("books/<int:pk>/", DetailView.as_view(), name="book-detail"),
    path("books/create/", CreateView.as_view(), name="book-create"),
    path("books/update/<int:pk>/", UpdateView.as_view(), name="book-update"),   # contains "books/update"
    path("books/delete/<int:pk>/", DeleteView.as_view(), name="book-delete"),   # contains "books/delete"
]
