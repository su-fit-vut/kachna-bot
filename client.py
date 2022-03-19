import disnake
from disnake.ext import commands
from pygame import mixer
from config import Config
import datetime, time
from iskachnaopen import IsKachnaOpen
import helper
import logging

class Bot(commands.Bot):
    def __init__(self):
        super().__init__()

        logging.info("Initializing pygame mixer")
        mixer.init()

    async def on_message(self, message):
        # Pokud uzivatel je bot, nebo jeste timeout pro klid mezi zvonenim, nebo je kachna otevrena
        # (chillzona, bar, atd...), tak nezvon, jen posli odpoved.

        if (
            message.author.bot
            or not (isinstance(message.channel, disnake.DMChannel) or self.user in message.mentions)
        ):
            return

        return
        logging.info(f"Incoming message from {message.author}.")
        
        # Recognize sound in message
        for sound_key in Config.sounds:
            if sound_key in message.content:
                if sound_key == "train":
                    await message.add_reaction('🚂')
                elif sound_key == "knock":
                    await message.add_reaction("🔔")
                else:
                    await message.add_reaction('☑️')
                logging.info("Playing sounds")
                ch = mixer.Channel(0)
                for s in Config.sounds[sound_key]:
                    while ch.get_queue():
                        time.sleep(1)
                    ch.queue(mixer.Sound(s))
                return
