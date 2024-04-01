from django.conf import settings
import  requests

SMS_KEY = settings.SMS_KEY_PASSWORD

def SendSms(message,contact,otp):
    message = message + " " + str(otp)
    sms_api = f"https://sms.vrittechnologies.com/smsapi/index?key={SMS_KEY}&contacts={contact}&senderid=SMSBit&msg={message}&responsetype=json"
    print(sms_api)
    response = requests.get(sms_api)
    print(response.json)
    return True
