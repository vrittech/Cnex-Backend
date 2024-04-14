from rest_framework.permissions import BasePermission
from accounts import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def AdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN, roles.SYSTEM_ADMIN]

def is_account_owner(request,view):
    # Check if the user owns the account being accessed
    instance = view.get_object()
    print(request.user.id, list(instance.to_notification.all().values_list('id',flat=True)))
    if len(request.data) == 1 and 'is_read' in request.data and request.user.id in list(instance.to_notification.all().values_list('id',flat=True)):
        return True
        
    return False

class NotificationPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        print(method_name)
        if method_name == 'create' or method_name == 'update':
            return AdminLevelPermission(request)
        elif method_name == 'partial_update':
            return is_account_owner(request,view)
        elif method_name == 'destroy':
            return False
        elif method_name == 'list' or method_name == 'retrieve':
            return True
        elif method_name in ["allReadNotification","notificationCount"]:
            return True        
        else:
            return False
            
        