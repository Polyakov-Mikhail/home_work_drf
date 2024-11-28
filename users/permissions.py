from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Сhecks if the user is a moderator"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(permissions.BasePermission):
    """Grants access only to the object owner"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
