from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.models import CustomUser

email_from = settings.EMAIL_HOST_USER

def sendMail(notification):
    print("order_delivered")
    if notification.get("notification_type") == "order_delivered":
        html_message = render_to_string('confirm_order.html')
        recipient_list = CustomUser.objects.filter(id__in = notification.get('to_notification')).values_list('email',flat=True)
        print(recipient_list)
        plain_message = ""
        subject = f"Order Received"
        send_mail(subject, plain_message, email_from, recipient_list,html_message=html_message)