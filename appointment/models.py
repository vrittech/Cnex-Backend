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
    
    def isServicesSlotsAvailable(self,date,slots):
        slots = self.slots.all().filter(id = slots)
        if slots.exists() == False:
            return False
        
        appointments = Appointment.objects.filter(checkout_appointment__services_items__service_id = self.id,checkout_appointment__services_items__slots_id = slots.first().id,checkout_appointment__services_items__appointment_date = date)
        available = slots.first().number_of_staffs - appointments.count()
        print(available," :: isServicesSlotsAvailable")
        return available>0
    
    def getServicesSlotsAvailable(self,date):
        slots = self.slots.all()
        slots_data = []
        for slot in slots:
            appointments = Appointment.objects.filter(checkout_appointment__services_items__service = self,checkout_appointment__services_items__slots = slot,checkout_appointment__services_items__appointment_date = date)
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

        print(services_detail, " :: getServicesSlotsAvailable")
           
        return services_detail
    
      
class Slots(models.Model): 
    services = models.ForeignKey(Services,related_name = 'slots',on_delete = models.CASCADE)
    from_time = models.TimeField()
    to_time = models.TimeField()
    number_of_staffs = models.IntegerField(default = 1)
    
    def __str__(self) -> str:
        return str(self.from_time) + "-" + str(self.to_time)
    
    def is_slots_available(self, date):
        appointments_count = Appointment.objects.filter(checkout_appointment__services_items__service = self.services,checkout_appointment__services_items__slots = self,checkout_appointment__services_items__appointment_date = date)
        return self.number_of_staffs - appointments_count > 0

class CheckoutAppointment(models.Model):
    total_price = models.PositiveIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

class ServicesItems(models.Model):
    checkout_appointment = models.ForeignKey(CheckoutAppointment,on_delete = models.PROTECT,related_name="services_items")
    service = models.ForeignKey(Services,related_name="appointments_items",on_delete = models.PROTECT) #Multiple servies, each services has price
    slots = models.ForeignKey(Slots,related_name="appointments_items",on_delete = models.PROTECT)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    appointment_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['checkout_appointment', 'slots'], name='checkout_service_slots_unique')
        ]

class Appointment(models.Model): #this is order
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT,related_name = "appointments_order")
    checkout_appointment = models.OneToOneField(CheckoutAppointment,on_delete=models.PROTECT,related_name = "appointments_order")
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status= models.CharField(max_length=255, choices=[
        ('paid','Paid'),
        ('unpaid','unpaid'),
    ],)

    appointment_status = models.CharField(max_length=255, choices=[
        ('confirmed','confirmed'),
        ('not-attened','Not Attened'),
        ('cancelled','cancelled'),
        ('checkout','cancelled'),
    ],default="checkout")

    payment_mode = models.CharField(max_length=255, choices=[
        ('esewa', 'Esewa'),
        ('khalti', 'Khalti'),
        ('fonepay', 'FonePay'),
        ('offline', 'offline'),
    ])
    cancellation_reason = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username


