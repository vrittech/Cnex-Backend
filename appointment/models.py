from django.db import models
from .models import *
from accounts.models import CustomUser
import uuid
# Create your models here.
class Slots(models.Model): #time #by admin
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    time_slot = models.CharField(max_length=255) #by admin, time slot list by admin
    number_of_staffs = models.IntegerField()
    date = models.DateField() #by admin, date list by admin
    
    def __str__(self) -> str:
        return str(self.time_slot) +" , "+ str(self.number_of_staffs) + " staff"

class Services(models.Model): #by admin
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name =  models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    slots = models.ManyToManyField(Slots) #if number of slots reached then, it raise errors slots not available.
    
    def __str__(self) -> str:
        return self.name + " " + str(self.price)

class Appointment(models.Model): #by users
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ManyToManyField(Services,related_name="Appointment") #Multiple servies, each services has price
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=255, choices=[
        ('esewa', 'Esewa'),
        ('khalti', 'Khalti'),
        ('fonepay', 'FonePay'),
    ])

    def __str__(self) -> str:
        return self.user.username + " " + str(self.service.first().name)

class BookedAppointment(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    cancellation_reason = models.TextField(null=True, blank=True)