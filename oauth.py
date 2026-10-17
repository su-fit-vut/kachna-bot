import time

import requests
from requests.auth import HTTPBasicAuth

from config import Config

# Global variables to store the cached token and its expiration time
cached_token = None
token_expiration = 0


def get_oauth_token(scope="kfm:e"):
    global cached_token, token_expiration

    # Check if a cached token exists and is still valid
    if cached_token and token_expiration > time.time():
        return cached_token
    auth = HTTPBasicAuth(Config.kis_client_id, Config.kis_client_secret)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"scope": scope, "grant_type": "client_credentials"}

    try:
        response = requests.post(
            Config.kis_token_endpoint,
            auth=auth,
            headers=headers,
            data=payload,
        )

        response_json = response.json()
        if response.status_code == 200:
            # Cache the new token and its expiration time
            cached_token = response_json.get("access_token")
            token_expiration = time.time() + response_json.get("expires_in")
            return cached_token
        else:
            print(
                "Error:",
                response_json.get(
                    "error", f"Unknown error {response.status_code}"
                ),
            )
            return None

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None
