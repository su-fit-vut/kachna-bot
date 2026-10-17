import logging

import disnake
from disnake.ext import commands

logger = logging.getLogger(__name__)


class Toasts(commands.Cog):
    @commands.slash_command(description="Zobrazí počet toustů.")
    async def toasts(
        self,
        inter: disnake.ApplicationCommandInteraction,
        number: int = commands.Param(
            ge=0,
            le=200,
            name="number",
            description="Počet toustů, 0 = došly",
            default=69,
        ),
    ):
        await inter.response.defer()
        message = "Toasty došly." if number == 0 else f"Toasty číslo {number}."
        logger.info("Toast count: %s", number)
        await inter.followup.send(f":white_check_mark: :sandwich: {message}")
