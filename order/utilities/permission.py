from rest_framework.permissions import BasePermission
from accounts import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN])

def AllLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN,roles.USER])

def ownerPermission(request,label):
    payload_user = getattr(request, label, None)
    print(payload_user)
    if request.user.id == payload_user.id:
        return True
    else:
        False

class AdminViewSetsPermission(BasePermission):
    def has_permission(self, request, view):
        return AdminLevel(request)
    
class WishlistPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['add_to_wishlist']:
            return True
        elif view.action in ['create','partial_update','update']:
            return False
        
        elif view.action in ['list','retrieve']:
            return AllLevel(request)
        
        else:
            return False
    
class CartPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create','partial_update','update']:
            return True
        elif view.action in ['list','retrieve']:
            return AllLevel(request)
        else:
            return False
    

        