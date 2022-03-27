import disnake
from disnake.ext import commands
from config import Config
from sound import Sound
import datetime
from kachnaonline import KachnaOnline
import helper
import logging


class Doorbell(commands.Cog):
    """
    Class for playing short sound in student club
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.sound = Sound(
            name="bell",
            files=[Config.sound_path]
        )
        self.wait_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=Config.wait_time)

    @commands.slash_command(description="Zakvákat v Kachně.")
    async def ring(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        """Rings in students' club"""
        await inter.response.defer()
        # await inter.response.send_message(':thinking: :bell:')
        next_available_call_at = self.wait_time + datetime.timedelta(seconds=Config.wait_time)
        if next_available_call_at > datetime.datetime.utcnow():
            next_call_at = helper.utc_to_local_time(next_available_call_at)
            await inter.response.send_message('Někdo jiný už před tebou zazvonil. Další zazvonění bude možné v: ' +
                                              f'**{helper.datetime_to_local_string(next_call_at)}**')
            return

        # if not KachnaOnline.is_closed():
        #     await inter.response.send_message('Kachna je otevřená a měl by mít volný průchod.')
        #     return

        self.wait_time = datetime.datetime.utcnow()
        logging.info("Playing sound")
        await inter.followup.send(
            content=":bell:"
        )
        self.sound.play()
