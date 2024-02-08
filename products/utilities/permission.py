from rest_framework.permissions import BasePermission
from accounts import roles

def IsAuthenticated(request):
    return bool(request.user and request.is_authenticated)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN])

class AdminViewSetsPermission(BasePermission):
    def has_permission(self, request, view):
        return AdminLevel(request)
        