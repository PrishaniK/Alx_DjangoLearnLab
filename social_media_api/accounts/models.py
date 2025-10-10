from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    """
    Custom user:
    - bio: short text
    - profile_picture: URL to avatar (keeps setup simple; no media config needed)
    - followers: users who follow this user (non-symmetrical self M2M)
    """
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)
    profile_image = models.ImageField(           
        upload_to="profiles/", blank=True, null=True
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def __str__(self):
        return self.username
