from rest_framework.permissions import BasePermission
from accounts import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]) and request.user.is_superuser

def AllLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN,roles.USER])    

class AdminViewSetsPermission(BasePermission):
    def has_permission(self, request, view):
        return AdminLevel(request)

class ShippingAddressViewsetsPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user,request.user.role)
        if  view.action in ['list','retrieve']:
            return True
        return AllLevel(request)
        