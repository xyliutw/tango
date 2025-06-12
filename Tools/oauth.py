# Tools/oauth.py

from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from jose import jwt as jose_jwt
import base64
import json

# ✅ Google
def verify_google_token(id_token: str) -> dict:
    try:
        idinfo = google_id_token.verify_oauth2_token(id_token, google_requests.Request())
        return idinfo
    except Exception as e:
        raise ValueError(f"Invalid Google token: {str(e)}")

# ✅ Apple（簡化版本，僅解析 JWT payload，不驗簽）
def verify_apple_token(id_token: str) -> dict:
    try:
        header, payload, signature = id_token.split(".")
        payload += "=" * (-len(payload) % 4)  # fix padding
        decoded = base64.urlsafe_b64decode(payload.encode("utf-8"))
        data = json.loads(decoded)
        return data
    except Exception as e:
        raise ValueError(f"Invalid Apple token: {str(e)}")
