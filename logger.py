import logging
import discord
import datetime
import requests
from config import Config


class Logger:
    @staticmethod
    def log_bell(message: discord.Message, trigger_type: str):
        data = {
            'dateTime': datetime.datetime.now().isoformat(),
            'source': trigger_type,
            'who': str(message.author)
        }

        request = requests.post(Config.service_config.logger, json=data)
        Logger.info('Log success: {}'.format(request.text))
        pass

    @staticmethod
    def info(message):
        logging.info(message)
