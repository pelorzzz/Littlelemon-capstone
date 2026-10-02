from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Any authenticated user can read (GET) menu items.
    Only users in the 'Manager' group can create/update/delete them.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Manager').exists()
