from rest_framework import viewsets, permissions, filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.utils import create_notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


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
        comment = serializer.save(author=self.request.user)
        # Notify the post author (avoid self-notify)
        post = comment.post
        if post.author_id != self.request.user.id:
            create_notification(recipient=post.author, actor=self.request.user, verb="commented on your post", target=post)

class FeedView(generics.ListAPIView):
    """
    GET /api/feed/  (Token auth)
    Returns posts authored by users current user follows, newest first.
    """
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")
    


class LikePostView(APIView):
    """
    POST /api/posts/<int:pk>/like/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)
        if post.author_id != request.user.id:
            create_notification(recipient=post.author, actor=request.user, verb="liked your post", target=post)
        return Response({"detail": "Liked."}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    """
    POST /api/posts/<int:pk>/unlike/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(post=post, user=request.user).delete()
        return Response({"detail": "Unliked."}, status=status.HTTP_200_OK)