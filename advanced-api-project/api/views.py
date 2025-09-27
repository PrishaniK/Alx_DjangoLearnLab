from rest_framework import viewsets, generics, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# - ListAPIView / RetrieveAPIView are read-only (AllowAny).
# - Create/Update/Destroy use IsAuthenticated and call perform_* hooks to normalize input.
# - Validation (e.g., future-year) is enforced by BookSerializer.

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().prefetch_related("books")
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related("author")
    serializer_class = BookSerializer

class BookListGV(generics.ListAPIView):
    """
    GET /api/gv/books/
    Read-only list of all books.
    """
    queryset = Book.objects.all().select_related("author")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # anyone can read

class BookDetailGV(generics.RetrieveAPIView):
    """
    GET /api/gv/books/<pk>/
    Read-only detail for one book.
    """
    queryset = Book.objects.all().select_related("author")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # anyone can read

class BookCreateGV(generics.CreateAPIView):
    """
    POST /api/gv/books/create/
    Create a new book (auth required).
    Uses serializer validation (future-year rule).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users

    def perform_create(self, serializer):
        # Example customization: normalize title before save
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)

class BookUpdateGV(generics.UpdateAPIView):
    """
    PUT/PATCH /api/gv/books/<pk>/update/
    Update an existing book (auth required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Example customization: normalize title
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)

class BookDeleteGV(generics.DestroyAPIView):
    """
    DELETE /api/gv/books/<pk>/delete/
    Delete a book (auth required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class ListView(generics.ListAPIView):
    """GET list of Books (public)."""
    queryset = Book.objects.all().select_related("author")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class DetailView(generics.RetrieveAPIView):
    """GET one Book (public)."""
    queryset = Book.objects.all().select_related("author")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class CreateView(generics.CreateAPIView):
    """POST create Book (auth required)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # small customization: normalize title
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)

class UpdateView(generics.UpdateAPIView):
    """PUT/PATCH update Book (auth required)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)

class DeleteView(generics.DestroyAPIView):
    """DELETE Book (auth required)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]