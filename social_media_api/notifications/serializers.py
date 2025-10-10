from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class ActorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorMiniSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "verb", "actor", "timestamp", "unread", "target_object_id")
