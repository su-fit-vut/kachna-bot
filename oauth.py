import json
import time

import requests
from requests.auth import HTTPBasicAuth

# Global variables to store the cached token and its expiration time
cached_token = None
token_expiration = 0


# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)


def get_oauth_token(scope="kfm:e"):
    global cached_token, token_expiration

    # Check if a cached token exists and is still valid
    if cached_token and token_expiration > time.time():
        return cached_token
    auth = HTTPBasicAuth(config["client_id"], config["secret"])
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"scope": scope, "grant_type": "client_credentials"}

    try:
        response = requests.post(
            config["url_token_endpoint"],
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
