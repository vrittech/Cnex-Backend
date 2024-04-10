from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.models import CustomUser
from order.models import Order

email_from = settings.EMAIL_HOST_USER

def sendMail(notification):
    print("order_delivered")
    if notification.get("notification_type") == "order_delivered":
        order_id = Order.objects.get(id = notification.get('object_id')).id
        html_message = render_to_string('confirm_order.html').format(order_id = order_id)
        recipient_list = CustomUser.objects.filter(id__in = notification.get('to_notification')).values_list('email',flat=True)
        print(recipient_list)
        plain_message = ""
        subject = f"Order Received"
        send_mail(subject, plain_message, email_from, recipient_list,html_message=html_message)