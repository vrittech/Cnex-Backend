from django.db import models
from .models import *
from accounts.models import CustomUser
import uuid
# Create your models here.


class Services(models.Model): #by admin
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name =  models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="appointment/services",blank=True,null=True)
    
    def __str__(self) -> str:
        return self.name + " " + str(self.price)
    
class Slots(models.Model): #time #by admin
    services = models.ForeignKey(Services,related_name = 'slots',on_delete = models.CASCADE)
    from_time = models.TimeField() #by admin, time slot list by admin
    to_time = models.TimeField() #by admin, time slot list by admin
    number_of_staffs = models.IntegerField(default = 1)
    
    def __str__(self) -> str:
        return str(self.from_time) + "-" + str(self.to_time)

class Appointment(models.Model): #by users
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Services,related_name="Appointment",on_delete = models.PROTECT) #Multiple servies, each services has price
    slots = models.ForeignKey(Slots,related_name="appointment",on_delete = models.PROTECT)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    appointment_date = models.DateField()
    payment_mode = models.CharField(max_length=255, choices=[
        ('esewa', 'Esewa'),
        ('khalti', 'Khalti'),
        ('fonepay', 'FonePay'),
    ])
    cancellation_reason = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username + " " + str(self.service.first().name)
