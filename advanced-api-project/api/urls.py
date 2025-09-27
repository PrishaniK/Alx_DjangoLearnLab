from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet
from .views import (
    AuthorViewSet, BookViewSet,
    BookListGV, BookDetailGV, BookCreateGV, BookUpdateGV, BookDeleteGV
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
]
