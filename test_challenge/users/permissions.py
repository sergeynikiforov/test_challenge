from rest_framework.permissions import IsAuthenticated
from rest_framework.compat import is_authenticated


class IsAuthenticatedAndIsAdminIfUpdated(IsAuthenticated):
    """
    Returns True for PUT only if is_admin is True and is_authenticated id True
    For other methods returns True only if is_authenticated is True
    """
    def has_permission(self, request, view):
        if request.method == 'PUT':
            return request.user and is_authenticated(request.user) and request.user.is_admin
        return request.user and is_authenticated(request.user)
