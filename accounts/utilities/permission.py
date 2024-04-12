from rest_framework.permissions import BasePermission
from accounts import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN])

def AllLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN,roles.USER])  

def ownerPermission(request,view,label):
    if request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
        return True
    
    payload_user = getattr(request, label, None)
    print(payload_user)
    if request.user.id == payload_user.id:
        return True
    else:
        False
        
class AdminViewSetsPermission(BasePermission):
    def has_permission(self, request, view):
        return AdminLevel(request)

class ShippingAddressViewsetsPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list','retrieve']:
            return True
        elif view.action in ['create','update','partial_update','destroy']:
            return ownerPermission(request,view,'profile')
        return False
    
def SecureFields(self,model_fields,secure_fields,secure_method,exceptions_roles):
    if self.context.get('request').method in secure_method and self.context.get('request').user.role not in exceptions_roles:
        for field in secure_fields:
            model_fields.get(field).read_only = True

    #request where user authentication is present
    #secure_fields which need to keep secure
    #methoods need secure for method like update,partial_update,create
    #roles: on which roles does not need strictions except given roles, all should need striction
    pass
        