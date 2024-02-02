# utils.py

from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings

GOOGLE_CLIENT_ID = '197998897092-qagliaukoha09ruuvjvae6q1gmb0b515.apps.googleusercontent.com'

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
        return None
