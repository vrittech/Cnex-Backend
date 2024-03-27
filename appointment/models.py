from django.db import models
from .models import *
from accounts.models import CustomUser
import uuid
from django.db.models import Count
# Create your models here.


class Services(models.Model): #by admin
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name =  models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="appointment/services",blank=True,null=True)
    is_active = models.BooleanField(default = True)
    
    def __str__(self) -> str:
        return self.name + " " + str(self.price)
    
    def getServicesSlotsAvailable(self,date):
        slots = self.slots.all()
        slots_data = []
        for slot in slots:
            appointments = slot.appointments.all().filter(appointment_date = date)
            available = slot.number_of_staffs - appointments.count()
            slots_data.append({
                'id':slot.id,
                'from_time':slot.from_time,
                'to_time':slot.to_time,
                'number_of_staffs':slot.number_of_staffs,
                'occupied':appointments.count(),
                'available':available,
                'is_available':available>0
            })

        services_detail = {
            'id':self.id,
            'name':self.name,
            'price':self.price,
            'slots':slots_data,
        }
           
        return services_detail
      
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
    service = models.ForeignKey(Services,related_name="appointments",on_delete = models.PROTECT) #Multiple servies, each services has price
    slots = models.ForeignKey(Slots,related_name="appointments",on_delete = models.PROTECT)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    appointment_date = models.DateField()
    payment_status= models.CharField(max_length=255, choices=[
        ('paid','Paid'),
        ('unpaid','unpaid'),
    ],)

    appointment_status = models.CharField(max_length=255, choices=[
        ('confirmed','confirmed'),
        ('not-attened','Not Attened'),
        ('cancelled','cancelled'),
    ],default="confirmed")

    payment_mode = models.CharField(max_length=255, choices=[
        ('esewa', 'Esewa'),
        ('khalti', 'Khalti'),
        ('fonepay', 'FonePay'),
        ('offline', 'offline'),
    ])
    cancellation_reason = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username + " " + str(self.service.name)
