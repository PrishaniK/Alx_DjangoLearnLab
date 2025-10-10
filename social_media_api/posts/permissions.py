from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Read: anyone.
    Write: only the object's author.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj has .author for both Post and Comment
        return getattr(obj, "author_id", None) == getattr(request.user, "id", None)
