from django.conf import settings

SMS_KEY = settings.SMS_KEY_PASSWORD

def SendSms(message,contact,otp):
    sms_api = f"https://sms.vrittechnologies.com/smsapi/index?key={SMS_KEY}&contacts={contact}&senderid=SMSBit&msg={message}&responsetype=json"
