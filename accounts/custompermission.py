from rest_framework.permissions import BasePermission
from . import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def AdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN, roles.SUPER_ADMIN]

class AccountPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            #check 
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False


class AdminLevelPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
           return AdminLevelPermission(request)
        elif method_name == 'retrieve':
            return AdminLevelPermission(request)
        elif method_name == 'update':
            return AdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False


class AllUserDataPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        # print(method_name)
        if method_name == 'list':
            return AdminLevelPermission(request)
        else:
            return False

    