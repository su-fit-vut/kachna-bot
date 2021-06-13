import requests
from config import Config
import logging
import time
import json


class IsKachnaOpen:
    @staticmethod
    def is_closed():
        logging.info('Checking IsKachnaOpen')
        start_time = time.time()

        state: str = IsKachnaOpen.get_state().strip()

        elapsed = round(time.time() - start_time, 2)
        logging.info(f'Checking IsKachnaOpen done. (Time: {elapsed} sec)')

        return state == 'Closed' or state == 'Private'

    @staticmethod
    def get_state() -> str:
        request = requests.get(Config.is_kachna_open, stream=True)
        return dict(json.loads(request.content))['state']
