import logging
from client import Bot
from config import Config

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")

        logging.info("Creating bot")
        bot = Bot()

        logging.info("Starting bot")
        bot.run(Config.key)
    except Exception as e:
        logging.error(str(e))
