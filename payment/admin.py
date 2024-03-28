from django.contrib import admin
from payment.models import Payment,PaymentService
# Register your models here.
admin.site.register([Payment,PaymentService])