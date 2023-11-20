import logging
import json

from client import Bot
from config import Config
from doorbell import Doorbell
from music import Music
from toasts import Toasts
from announcer import Announce
from signalrcore.hub_connection_builder import HubConnectionBuilder
# from signalrcore.hub.errors import HubConnectionError
from oauth import get_oauth_token

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")

        logging.info("Creating bot")
        bot = Bot()
        bot.add_cog(Doorbell(bot))
        bot.add_cog(Music(bot))
        bot.add_cog(Toasts(bot))
        bot.add_cog(Announce(bot))

        # Load configuration from JSON file
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

        # Access configuration values
        url_signalr = config["url_signalr"]
        keep_alive_interval = config["keep_alive_interval"]
        reconnect_interval = config["reconnect_interval"]

        async def announce_ticket(itemDetails):
            if len(itemDetails) == 0:
                return
            item = itemDetails[0]
            a = Announce(bot)
            await a.order(
                None,
                item['number'],
                item['customerName']
            )
        
        def create_async_task(itemDetails):
            logging.info(bot.loop)
            bot.loop.create_task(announce_ticket(itemDetails))


        hub_connection = (
            HubConnectionBuilder()
            .with_url(
                url_signalr,
                options={
                    "access_token_factory": get_oauth_token,
                    "headers": {"Authorization": "token"},
                },
            )
            .configure_logging(logging.ERROR)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": keep_alive_interval,
                    "reconnect_interval": reconnect_interval,
                    "max_attempts": None,  # infinite attempts
                }
            )
            .build()
        )

        hub_connection.on_open(lambda: logging.info("Connected to the server."))
        hub_connection.on_reconnect(lambda: logging.info("reconnection in progress"))

        hub_connection.on("ReadyToCollect", create_async_task)

        hub_connection.start()
        hub_connection.on_close(lambda: hub_connection.start())

        logging.info("Starting bot")
        bot.run(Config.key)
    except Exception as e:
        logging.error(str(e))
