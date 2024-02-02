from rest_framework.permissions import BasePermission
from account import roles


def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def is_account_owner(user, request):
    print(request.data.get('user'),"::",user.id)
    bool_data = str(request.data.get('followed_by_user')) == str(user.id)
    return bool_data

def AdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN, roles.SYSTEM_ADMIN]

class AccountPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        # print(method_name)
        if method_name == 'list':
            return True
        elif method_name == 'create':
            #check 
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            #check update role , if  role is user then only can updte there own account. for update all role must be ADMIN
            return True
        elif method_name == 'partial_update':
            return True
        elif method_name == 'destroy':
            return False
        else:
            return False

class RelationshipPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        # print(method_name)
        if method_name == 'list':
            return True
        elif method_name == 'create':
            user = request.user,
            return  is_account_owner(request.user, request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            user = request.user,
            return  is_account_owner(request.user, request)
        elif method_name == 'partial_update':
            user = request.user,
            return  is_account_owner(request.user, request)
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

    