import requests
from config import Config
import logging
import time
import json


class KachnaOnline:
    @staticmethod
    def is_closed():
        logging.info("Checking KachnaOnline API")
        start_time = time.time()

        state: str = KachnaOnline().get_state().strip()

        elapsed = round(time.time() - start_time, 2)
        logging.info(f"Checking KachnaOnline API done. (Time: {elapsed} sec)")

        return state == "Closed" or state == "Private"

    @staticmethod
    def get_state() -> str:
        request = requests.get(Config.is_kachna_open, stream=True)
        return dict(json.loads(request.content))["state"]
