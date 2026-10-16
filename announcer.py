import logging

import disnake
from disnake.ext import commands

logger = logging.getLogger(__name__)


class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Zobrazí objednávku.")
    async def order(
        self,
        inter: disnake.ApplicationCommandInteraction | None,
        number: int = commands.Param(
            ge=0,
            le=99,
            name="number",
            description="Číslo objednávky",
            default=69,
        ),
        recipient: str = commands.Param(
            name="recipient",
            description="Jméno příjemce objednávky",
            default=None,
        ),
    ):
        if recipient is None:
            response_text = str(number)
            if number == 69:
                response_text += " <:nepSmug:827833315822141451>"
            elif number == 0:
                response_text = "<:sadIvo:567039959257710592>"
        else:
            response_text = f":arrow_right: \"{recipient}\""

        logger.info("Food order %s for %s", number, recipient or "unspecified recipient")
        if inter is not None:
            await inter.response.defer()
            await inter.followup.send(f":white_check_mark: :sandwich: Order {response_text}")
