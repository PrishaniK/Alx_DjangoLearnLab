from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(*, recipient, actor, verb, target=None):
    kwargs = {
        "recipient": recipient,
        "actor": actor,
        "verb": verb,
    }
    if target is not None:
        kwargs["target_content_type"] = ContentType.objects.get_for_model(type(target) if not hasattr(target, "_meta") else target)
        # If target passed is a model instance, ^ works. If you pass a class, adjust accordingly.
        # Simpler:
        if hasattr(target, "_meta"):
            kwargs["target_content_type"] = ContentType.objects.get_for_model(target)
            kwargs["target_object_id"] = target.pk
        else:
            # Fallback: no target id
            kwargs.pop("target_content_type", None)
    return Notification.objects.create(**kwargs)
