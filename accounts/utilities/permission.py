from rest_framework.permissions import BasePermission
from accounts import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN])

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
    
def SecureFields(self,model_fields,secure_fields,secure_method,exceptions_roles):
    if self.context.get('request').method in secure_method and self.context.get('request').user.role not in exceptions_roles:
        print(" inside checking ")
        for field in secure_fields:
            model_fields.get(field).read_only = True

    #request where user authentication is present
    #secure_fields which need to keep secure
    #methoods need secure for method like update,partial_update,create
    #roles: on which roles does not need strictions except given roles, all should need striction
    pass
        