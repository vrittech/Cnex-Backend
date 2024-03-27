from appointment.models import Services
# "services":[{"service":14,"slots":35,"appointment_date":"2024-03-27","user":3}]
def checkServicesAvailable(datas):
    for data in datas:
        service_obj = Services.objects.filter(id = data.get('service'))
        if not service_obj.exists():
            return False
        
        appointment_date = data.get('appointment_date')
        slots = data.get('slots')

        if not appointment_date or not slots:
            return False
        
        return service_obj.first().isServicesSlotsAvailable(appointment_date,slots)
