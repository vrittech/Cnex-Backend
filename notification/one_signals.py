import requests
api_key = "YzliYWI5YjUtODRkMC00MmIwLWFhZmItZjczYjExYjk1Yjc1"
api_key = "YzliYWI5YjUtODRkMC00MmIwLWFhZmItZjczYjExYjk1Yjc1"
url = "https://onesignal.com/api/v1/notifications"

def sendNotificationToOneSignals(data):
    
    headers = {
        "Authorization": f"Basic {api_key}",
        "app_id":"cc098330-e95b-44f5-ab5f-934c99a60c28",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    print(data.get('to_notification'))
    payload = {
        "app_id":"cc098330-e95b-44f5-ab5f-934c99a60c28",
        "included_segments":['30'],#data.get('to_notification'),
        "contents": {"en": data.get('notification_message'), "es": data.get('notification_message')}
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text)

    #     response.raise_for_status()
    #     print("Notification sent successfully!")
    # except requests.exceptions.RequestException as e:
    #     print("Failed to send notification:", e)
