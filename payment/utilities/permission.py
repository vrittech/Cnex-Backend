from rest_framework.permissions import BasePermission
from accounts import roles
from order.models import Order
from appointment.models import CheckoutAppointment

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]) and request.user.is_superuser

def isOwner(request):
    order = Order.objects.filter(id = request.data.get('order_id'))
    if not order.exists():
        return False
    if request.user.id == order.first().user.id:
        return True
    return False


def isServiceOwner(request):
    order = CheckoutAppointment.objects.filter(id = request.data.get('order_id'))
    print(order, " permission ")
    if not order.exists():
        return False
    if request.user.id == order.first().user.id:
        return True
    return False
    
class AdminViewSetsPermission(BasePermission):
    def has_permission(self, request, view):
        return AdminLevel(request)

class PaymentVerifyPermission(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticated(request) and isOwner(request)
        
class ServicePaymentVerifyPermission(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticated(request) and isServiceOwner(request)
        