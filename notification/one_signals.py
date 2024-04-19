import requests
from django.conf import settings

url = "https://onesignal.com/api/v1/notifications"

def sendNotificationToOneSignals(data,file = None):
    print(file, " :: file")
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {settings.ONE_SIGNAL_API_KEY}",
        "content-type": "application/json"
    }
    print(data.get('to_notification'))
    if data.get('notification_type') in ['product_push_notification','static_push_notification','collection_push_notification']:
        payload = {
            "app_id":settings.APP_ID,
            "contents": {"en": data.get('notification_message'),},
            # "included_segments":["Subscribed Users"],#["Active Users", "Inactive Users"],
            "filters": [{"field": "country","relation": "=", "value": "NP"}],
            "headings": {"en": data.get('title'),},
            "url":data.get('url'),
            "big_picture":file,
            "data":{"path":data.get('path')}
        }
    else:
        payload = {
            "app_id":settings.APP_ID,
            "contents": {"en": data.get('notification_message'),},
            "filters": [{"field": "tag", "key": "user_id", "relation": "=", "value": data.get('to_notification')[0]},],
            "data":{"path":data.get('path')}
        }

       
    print(data.get('notification_type') ,"\n",payload)
    response = requests.post(url, headers=headers, json=payload)
    print(response.text, " response ")
    #     response.raise_for_status()
    #     print("Notification sent successfully!")
    # except requests.exceptions.RequestException as e:
    #     print("Failed to send notification:", e)


