import requests
from config import Config
from logger import Logger
import time
import json


class IsKachnaOpen:
    @staticmethod
    def is_closed():
        Logger.info('Checking IsKachnaOpen')
        start_time = time.time()

        state: str = IsKachnaOpen.get_state().strip()

        elapsed = round(time.time() - start_time, 2)
        Logger.info('Checking IsKachnaOpen done. (Time: {} sec)'.format(elapsed))

        return state == 'Closed' or state == 'Private'

    @staticmethod
    def get_state() -> str:
        request = requests.get(Config.service_config.iskachnaopen, stream=True)
        response = dict(json.loads(request.content))
        return response['state']
