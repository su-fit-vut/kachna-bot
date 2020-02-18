import discord
import logging
from client import Bot
from config import Config

if __name__ == "__main__":
    try:
        logging.basicConfig(filename='all.log',level=logging.INFO)

        logging.info("Creating bot")
        bot = Bot(Config.sound_path)

        logging.info("Starting bot")
        bot.run(Config.key)
    except Exception as e:
        logging.error(str(e))

