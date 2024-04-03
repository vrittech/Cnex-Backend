# utils.py

from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings

# GOOGLE_CLIENT_ID = '976671591908-6mbvs6crsd63pd571781sihul4qc40hi.apps.googleusercontent.com'
# GOOGLE_CLIENT_ID = '976671591908-sugqc0jsn1e4fasbhmnoe4rmcvk1665l.apps.googleusercontent.com'
# GOOGLE_CLIENT_ID = '976671591908-c496ffugo7650vm3k8kegrv4sd6rg34t.apps.googleusercontent.com'
GOOGLE_CLIENT_ID = "109885216359799829993"

def VerifyGoogleToken(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        # Check that the token is valid for this app
        if idinfo['aud'] not in [GOOGLE_CLIENT_ID]:
            raise ValueError('Invalid audience.')
        return idinfo,True
    except ValueError as e:
        # Invalid token
        print(f'Error verifying Google ID token: {e}')
        return None,False


# Example usage for validating authorization code
client_id = 'com.vrit.cnex'
client_secret = 'YOUR_CLIENT_SECRET'
# code = 'AUTHORIZATION_CODE'
redirect_uri = 'YOUR_REDIRECT_URI'

def VerifyAppleToken(token):
    url = "https://appleid.apple.com/auth/token"
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': token,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

def validate_refresh_token():
    refresh_token = 'REFRESH_TOKEN'
    url = "https://appleid.apple.com/auth/token"
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

def generateSecreteKey(request):

    import jwt
    from time import timezone
    from datetime import timedelta,datetime

    headers = {'kid': settings.APPLE_CLIENT_ID}

    payload = {'iss': settings.APPLE_TEAM_ID,
    'iat': datetime.now(),
    'exp': datetime.now() + timedelta(days=180),
    'aud': 'https://appleid.apple.com',
    'sub': settings.APPLE_CLIENT_ID,
    }
    
    client_secret = jwt.encode(
            payload, 
            settings.APPLE_PRIVATE_KEY, 
            algorithm='ES256', 
            headers=headers
        ).decode("utf-8")
    
    print(client_secret)
    return client_secret

