from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class CustomPermission(BasePermission):
    """
    """
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS) or request.user.is_staff:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Only user with staff permission can add/edit/delete
        Rest user can only get the object/s.
        """
        if (request.method in SAFE_METHODS) or request.user.is_staff:
            return True

        return False


class CustomStrictPermission(BasePermission):
    """
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Only user with staff permission can add/edit/delete
        Rest user can only get the object/s.
        """
        if request.user.is_staff:
            return True

        return False
