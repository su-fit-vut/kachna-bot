import disnake
from disnake.ext import commands
from config import Config
from os.path import exists
from sound import Sound
import requests
from pydub import AudioSegment
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
        number: int = commands.Param(
            ge=0,
            le=200,
            name="number",
            description="číslo volaných toustů"
        ),
        # recipient: str = commands.Param(
        #     name="recipient",
        #     description="jméno příjemce volaných toustů",
        #     default=None
        # ),
        lang: str = commands.Param(
            name="language",
            description="jazyk pro vyhlášení toustů",
            default="cs-CZ",
            choices=["cs-CZ", "en-US", "sk-SK"]
        )
    ):
        await inter.response.defer()

        logging.info(f"Going to declare toasts {number} in {lang}.")
        full_filename = f"toasts-{lang}-{number}.wav"
        if lang == "cs-CZ":
            text = f"Toasty číslo {number}"
            flag_emote = ":flag_cz:"
            if number == 69:
                text = "Toasty číslo 69    Naaajssss"
        elif lang == "en-US":
            text = f"Toast number {number}"
            flag_emote = ":flag_us:"
            if number == 69:
                text = "Toasts number 69    Nice"
        elif lang == "sk-SK":
            text = f"Tousty číslo {number}"
            flag_emote = ":flag_sk:"
            if number == 69:
                text = "Toasty číslo 69    Naajsss"

        if not exists(full_filename):
            # If file is not in local directory create it
            q = requests.utils.quote(text)
            request = requests.get(
                f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={q}"
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
            content=f":white_check_mark: :sandwich: {number} {flag_emote}"
        )
