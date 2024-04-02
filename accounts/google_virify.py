# utils.py

from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings

# GOOGLE_CLIENT_ID = '976671591908-6mbvs6crsd63pd571781sihul4qc40hi.apps.googleusercontent.com'
GOOGLE_CLIENT_ID = '976671591908-sugqc0jsn1e4fasbhmnoe4rmcvk1665l.apps.googleusercontent.com'

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
