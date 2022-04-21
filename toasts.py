import disnake
from disnake.ext import commands
from config import Config
from os.path import exists
from sound import Sound
import requests
from pydub import AudioSegment
import time
import logging


class Toasts(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot

    @commands.slash_command(description="Vyhlásí tousty.")
    async def toasts(
        self,
        inter: disnake.ApplicationCommandInteraction,
        number: str = commands.Param(name="number")
    ):
        """
        Parameters
        ----------
        number: číslo volaných toustů
        """
        await inter.response.defer()

        logging.info(f"Going to declare toasts {number}")
        full_filename = f"tousty_cislo_{number}.wav"
        text = f"Toasty číslo {number}"
        if number == "69":
            text = f"Toasty číslo 69    Naaajssss"
        if not exists(full_filename):
            # If file is not in local directory create it
            request = requests.get(
                f"https://translate.google.com/translate_tts?ie=UTF-8&tl=cs-CZ&client=tw-ob&q={requests.utils.quote(text)}"
            )
            open(f"{Config.toasts_sounds_path}/{full_filename[:-4]}.mp3", "wb").write(request.content)

            # convert wav to mp3
            sound = AudioSegment.from_mp3(f"{Config.toasts_sounds_path}/{full_filename[:-4]}.mp3")
            sound.export(f"{Config.toasts_sounds_path}/{full_filename}", format="wav")

        sound_to_play = Sound(
            name=text,
            files=[
                f"{Config.toasts_sounds_path}/{full_filename}"
            ],
            spotify=Config.spotify,
        )

        # Play the sound
        sound_to_play.play_fade_out()

        # Update message
        await inter.followup.send(
            content=f":white_check_mark: :sandwich: {number}"
        )
