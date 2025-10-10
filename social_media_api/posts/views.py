from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """
    list, retrieve: public
    create/update/delete: owner only (auth)
    Filtering: search by title/content, order by created_at/title
    """
    queryset = Post.objects.all().select_related("author")
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination

    # Filtering / Search / Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "title", "updated_at", "id"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    list, retrieve: public
    create/update/delete: owner only (auth)
    Supports nested create when `post` is provided in payload.
    """
    queryset = Comment.objects.all().select_related("author", "post")
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination

    def perform_create(self, serializer):
        # expects {"post": <post_id>, "content": "..."}
        serializer.save(author=self.request.user)

