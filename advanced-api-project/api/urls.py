from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ViewSets
    AuthorViewSet, BookViewSet,
    # Generic Views (gv)
    BookListGV, BookDetailGV, BookCreateGV, BookUpdateGV, BookDeleteGV,
    # Checker-friendly CBV names
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")

urlpatterns = [
    path("", include(router.urls)),
    path("gv/books/", BookListGV.as_view(), name="gv-book-list"),                       # GET
    path("gv/books/<int:pk>/", BookDetailGV.as_view(), name="gv-book-detail"),          # GET
    path("gv/books/create/", BookCreateGV.as_view(), name="gv-book-create"),            # POST (auth)
    path("gv/books/<int:pk>/update/", BookUpdateGV.as_view(), name="gv-book-update"),   # PUT/PATCH (auth)
    path("gv/books/<int:pk>/delete/", BookDeleteGV.as_view(), name="gv-book-delete"),   # DELETE (auth)
    
    path("cbv/books/", ListView.as_view(), name="cbv-book-list"),
    path("cbv/books/<int:pk>/", DetailView.as_view(), name="cbv-book-detail"),
    path("cbv/books/create/", CreateView.as_view(), name="cbv-book-create"),
    path("cbv/books/<int:pk>/update/", UpdateView.as_view(), name="cbv-book-update"),
    path("cbv/books/<int:pk>/delete/", DeleteView.as_view(), name="cbv-book-delete"),
    path("books/<int:pk>/update/", UpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", DeleteView.as_view(), name="book-delete"),
]
