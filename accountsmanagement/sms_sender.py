
SMS_KEY = ""

def SendSms(message,contact):
    sms_api = f"https://sms.vrittechnologies.com/smsapi/index?key={SMS_KEY}&contacts={contact}&senderid=SMSBit&msg={message}&responsetype=json"
