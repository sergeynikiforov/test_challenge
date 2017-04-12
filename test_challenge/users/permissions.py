from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.compat import is_authenticated


class IsAuthenticatedAndIsAdminOrSelfIfUserChanged(IsAuthenticated):
    """
    Returns True for unsafe methods only if:
     - (is_admin is True OR request.user is the obj) AND is_authenticated id True
    For other methods returns True only if is_authenticated is True (relies on inheritance)
    """
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user.pk == obj.pk or request.user.is_admin
        return True


class IsAuthenticatedAndIsMemberIfTeamChanged(IsAuthenticated):
    """
    Returns True for unsafe methods only if User is a member of a team
    """
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user and is_authenticated(request.user) and request.user.team == obj
        return True
