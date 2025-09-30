from django.db import models
from django.conf import settings

class Post(models.Model):
    """
    A simple blog post.
    - author: links to Django's User (supports many posts per user)
    - published_date: auto-set when created
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title
