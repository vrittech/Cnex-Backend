from django.contrib import admin
from payment.models import Payment,PaymentService,PaymentFail
# Register your models here.
admin.site.register([Payment,PaymentService,PaymentFail])