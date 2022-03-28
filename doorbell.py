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
        self.sound = Sound(
            name="bell",
            files=[Config.sound_path],
            spotify=Config.spotify,
        )
        self.wait_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=Config.wait_time)

    @commands.slash_command(description="Zakvákat v Kachně.")
    async def ring(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        """Rings in students' club"""
        await inter.response.defer()

        logging.info("Going to ring in the club if can")
        # Check if somebody did not ring before you
        next_available_call_at = self.wait_time + datetime.timedelta(seconds=Config.wait_time)
        if next_available_call_at > datetime.datetime.utcnow():
            next_call_at = helper.utc_to_local_time(next_available_call_at)
            await inter.followup.send(
                content="Někdo jiný už před tebou zazvonil. Další zazvonění bude možné v: " +
                f"**{helper.datetime_to_local_string(next_call_at)}**")
            return

        # Check student club is not opened
        if not KachnaOnline.is_closed():
            await inter.followup.send(
                content="Kachna je otevřená a měl by mít volný průchod."
            )
            return

        self.wait_time = datetime.datetime.utcnow()
        self.sound.play_fade_out()
        await inter.followup.send(
            content=":bell:"
        )
