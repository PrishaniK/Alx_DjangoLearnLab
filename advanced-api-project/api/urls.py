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
    # --- CBVs FIRST to avoid router catching "create" as a pk ---
    path("books/", ListView.as_view(), name="book-list"),
    path("books/create/", CreateView.as_view(), name="book-create"),
    path("books/update/<int:pk>/", UpdateView.as_view(), name="book-update"),
    path("books/delete/<int:pk>/", DeleteView.as_view(), name="book-delete"),
    path("books/<int:pk>/", DetailView.as_view(), name="book-detail"),

    # Router endpoints AFTER
    path("", include(router.urls)),
]
