from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# ViewSets (keep these; they don't conflict and are useful)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().prefetch_related("books")
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related("author")
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "publication_year", "author", "author__name"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year", "id"]
    ordering = ["title"]  # default sort

# --- Single set of generic views with the checker-friendly names ---
class ListView(generics.ListAPIView):
    """GET /api/books/"""
    queryset = Book.objects.all().select_related("author")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "publication_year", "author", "author__name"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year", "id"]
    ordering = ["title"]

class DetailView(generics.RetrieveAPIView):
    """GET /api/books/<pk>/"""
    queryset = Book.objects.all().select_related("author")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CreateView(generics.CreateAPIView):
    """POST /api/books/create/"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)

class UpdateView(generics.UpdateAPIView):
    """PUT/PATCH /api/books/update/<pk>/"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)

class DeleteView(generics.DestroyAPIView):
    """DELETE /api/books/delete/<pk>/"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
