import json
import logging
import time

import requests

from config import Config

logger = logging.getLogger(__name__)


class KachnaOnline:
    @staticmethod
    def is_closed():
        logger.info("Checking KachnaOnline API")
        start_time = time.time()

        state: str = KachnaOnline().get_state().strip()

        elapsed = round(time.time() - start_time, 2)
        logger.info("Checking KachnaOnline API done. (Time: %s sec)", elapsed)

        return state == "Closed" or state == "Private"

    @staticmethod
    def get_state() -> str:
        request = requests.get(Config.kachnaonline_url, stream=True)
        return dict(json.loads(request.content))["state"]
