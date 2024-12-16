from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission that allows access only to resources belonging to the user
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
