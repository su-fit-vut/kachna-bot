import logging
from os.path import exists
import requests

from config import Config
from sound import Sound
from pydub import AudioSegment
import disnake
from disnake.ext import commands


class Announce(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot

    @commands.slash_command(description="Vyhlásí objednávku.")
    async def order(
        self,
        inter: disnake.ApplicationCommandInteraction | None,
        number: int = commands.Param(
            ge=0,
            le=99,
            name="number",
            description="Číslo volaných toustů, 0 = došly",
            default=69
        ),
        recipient: str = commands.Param(
            name="recipient",
            description="Jméno příjemce volaných toustů v 2. pádě (Pro koho? Čeho?)",
            default=None
        )
    ):
        if inter is not None:
            await inter.response.defer()

        # Prepare variables for order announcement
        text = f".   objednávka číslo {number}"
        if recipient is not None:
            # Recipient way
            logging.info(f"Going to announce order number \"{recipient}\" for \"{recipient}\".")
            full_filename = f"order-for-recipient-{number}.wav"
            text += f" pro uživatele {recipient}."
            response_text = f":arrow_right: \"{recipient}\""
        else:
            # Number way
            logging.info(f"Going to announce order number \"{recipient}\".")
            full_filename = f"order-for-recipient-{number}.wav"
            response_text = str(number)
            if number == 69:
                response_text = f"{number} <:nepSmug:827833315822141451>"
            elif number == 0:
                response_text = "<:sadIvo:567039959257710592>"

        # If file is not in local directory create it
        if not exists(full_filename):
            q = requests.utils.quote(text)
            request = requests.get(
                f"https://translate.google.com/translate_tts?ie=UTF-8&tl=cs-CZ&client=tw-ob&q={q}"
            )
            open(f"{Config.toasts_sounds_path}/{full_filename[:-4]}.mp3", "wb").write(request.content)

            # convert wav to mp3
            sound = AudioSegment.from_mp3(f"{Config.toasts_sounds_path}/{full_filename[:-4]}.mp3")
            sound.export(f"{Config.toasts_sounds_path}/{full_filename}", format="wav")

        # Define sound object
        sound_to_play = Sound(
            name=text,
            files=[
                f"{Config.toasts_sounds_path}/{full_filename}"
            ],
            spotify=Config.spotify,
        )

        # Play the sound object
        sound_to_play.play_fade_out()

        if inter is not None:
            # Send response message to channel
            await inter.followup.send(
                content=f":white_check_mark: :sandwich: {response_text}"
            )
