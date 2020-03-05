import discord
from pygame import mixer
from config import Config
import datetime
from iskachnaopen import IsKachnaOpen
from logger import Logger
import helper


class Bot(discord.Client):
    def __init__(self):
        super().__init__()

        Logger.info("Initializing pygame mixer")
        mixer.init()

        Logger.info("Creating sound object")
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

        Logger.info("Incoming message from {}.".format(message.author))
        next_available_call_at = self.wait_time + datetime.timedelta(seconds=Config.wait_time)
        if next_available_call_at > datetime.datetime.utcnow():
            await message.add_reaction('❌')
            await message.channel.send('Někdo jiný už před tebou zazvonil. Další zazvonění bude možné v: {}'
                                       .format(helper.datetime_to_local_string(next_available_call_at)))
            return

        if not IsKachnaOpen.is_closed():
            await message.add_reaction('❌')
            await message.channel.send('Kachna je otevřená a měl by mít volný průchod.')
            return

        if isinstance(message.channel, discord.DMChannel):
            Logger.log_bell(message, 'PM')
        elif self.user in message.mentions:
            Logger.log_bell(message, 'Guild')
        else:
            return

        self.wait_time = datetime.datetime.utcnow()
        await message.add_reaction('✅')
        Logger.info("Playing sound")
        self.sound.play()
