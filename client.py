import discord
import logging
from pygame import mixer
from config import Config
import datetime


class Bot(discord.Client):
    def __init__(self):
        super().__init__()

        logging.info("Initializing pygame mixer")
        mixer.init()

        logging.info("Creating sound object")
        self.sound = mixer.Sound(Config.sound_path)
        self.wait_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=Config.wait_time)

    async def on_message(self, message):
        if(
            message.author.bot or
            self.wait_time + datetime.timedelta(seconds=Config.wait_time) > datetime.datetime.utcnow()
        ):
            return

        logging.info("Incoming message from {}.".format(message.author))
        if isinstance(message.channel, discord.DMChannel) or self.user in message.mentions:
            self.wait_time = datetime.datetime.utcnow()
            logging.info("Playing sound")
            self.sound.play()
