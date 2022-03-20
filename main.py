import logging
from client import Bot
from config import Config
from doorbell import Doorbell
from music import Music

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")

        logging.info("Creating bot")
        bot = Bot()
        bot.add_cog(Doorbell(bot))
        bot.add_cog(Music(bot))

        logging.info("Starting bot")
        bot.run(Config.key)
    except Exception as e:
        logging.error(str(e))
