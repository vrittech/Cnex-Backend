import requests
from django.conf import settings

url = "https://onesignal.com/api/v1/notifications"

def sendNotificationToOneSignals(data):
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {settings.ONE_SIGNAL_API_KEY}",
        "content-type": "application/json"
    }
    print(data.get('to_notification'))
    payload = {
        "app_id":settings.APP_ID,
        "filters": [
            {"field": "tag", "key": "user_id", "relation": "=", "value": data.get('to_notification')},
        ],
        "contents": {"en": data.get('notification_message'), "es": data.get('notification_message')}
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text)

    #     response.raise_for_status()
    #     print("Notification sent successfully!")
    # except requests.exceptions.RequestException as e:
    #     print("Failed to send notification:", e)


