import requests
from django.conf import settings

url = "https://onesignal.com/api/v1/notifications"

def sendNotificationToOneSignals(data):
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {settings.ONE_SIGNAL_API_KEY}",
        "content-type": "application/json"
    }
    # print(data.get('to_notification'))
    filters_array = []
    for to_notification in data.get('to_notification'):
        filters_array.append({"field": "tag", "key": "user_id", "relation": "=", "value": to_notification})
    payload = {
        "app_id":settings.APP_ID,
        "filters": filters_array,
        "contents": {"en": data.get('notification_message'),},
        "data":{"path":data.get('path')}
    }

    print(payload)
    response = requests.post(url, headers=headers, json=payload)
    #     response.raise_for_status()
    #     print("Notification sent successfully!")
    # except requests.exceptions.RequestException as e:
    #     print("Failed to send notification:", e)


