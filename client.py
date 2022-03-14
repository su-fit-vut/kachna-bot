import discord
from pygame import mixer
from config import Config
import datetime, time
from iskachnaopen import IsKachnaOpen
import helper
import logging

class Bot(discord.Client):
    def __init__(self):
        super().__init__()

        logging.info("Initializing pygame mixer")
        mixer.init()

        logging.info("Creating sound object")
        self.sound = mixer.Sound(Config.sound_path)
        self.wait_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=Config.wait_time)

    async def on_message(self, message):
        # Pokud uzivatel je bot, nebo jeste timeout pro klid mezi zvonenim, nebo je kachna otevrena
        # (chillzona, bar, atd...), tak nezvon, jen posli odpoved.

        if (
            message.author.bot
            or not (isinstance(message.channel, discord.DMChannel) or self.user in message.mentions)
        ):
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

        next_available_call_at = self.wait_time + datetime.timedelta(seconds=Config.wait_time)
        if next_available_call_at > datetime.datetime.utcnow():
            await message.add_reaction('❌')
            next_call_at = helper.utc_to_local_time(next_available_call_at)
            await message.channel.send('Někdo jiný už před tebou zazvonil. Další zazvonění bude možné v: ' +
                                       f'**{helper.datetime_to_local_string(next_call_at)}**')
            return

        if not IsKachnaOpen.is_closed():
            await message.add_reaction('❌')
            await message.channel.send('Kachna je otevřená a měl by mít volný průchod.')
            return

        self.wait_time = datetime.datetime.utcnow()
        await message.add_reaction('✅')
        logging.info("Playing sound")
        self.sound.play()
