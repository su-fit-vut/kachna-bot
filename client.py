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
        if self.wait_time + datetime.timedelta(seconds=Config.wait_time) > datetime.datetime.utcnow():
            return
        self.wait_time = datetime.datetime.utcnow()

        if isinstance(message.channel, discord.DMChannel):
            self.play_sound()
        else:
            if self.user in message.mentions and message.channel.id == Config.allowed_channel:
                self.play_sound()

    def play_sound(self):
        logging.info("Playing sound")
        self.sound.play()

