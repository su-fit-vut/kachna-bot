import discord
import logging
from pygame import mixer

class Bot(discord.Client):
    def __init__(self, sound_path):
        super().__init__()

        logging.info("Initializing pygame mixer")
        mixer.init()

        logging.info("Creating sound object")
        self.sound = mixer.Sound(sound_path)

    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            self.play_sound()
        else:
            if self.user in message.mentions:
                self.play_sound()

    def play_sound(self):
        logging.info("Playing sound")
        self.sound.play()

