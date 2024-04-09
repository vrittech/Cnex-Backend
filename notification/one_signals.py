import requests
api_key = "YzliYWI5YjUtODRkMC00MmIwLWFhZmItZjczYjExYjk1Yjc1"
url = "https://onesignal.com/api/v1/notifications"

def sendNotificationToOneSignals(data):
    
    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "included_segments":data.get('to_notification'),
        "contents": {"user_message": data.get('notification_message'), "admin_message": data.get('notification_message')}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("Notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print("Failed to send notification:", e)
