import asyncio
import logging
from os.path import exists
from pathlib import Path

import disnake
import requests
from disnake.ext import commands
from pydub import AudioSegment

from config import Config
from sound import Sound

logger = logging.getLogger(__name__)


class ToastLanguage:
    def __init__(
        self,
        name: str,
        flag_emote: str,
        default_toasts_text: str,
        special_toasts_text: str,  # 69
        recipient_toasts_text: str,
        gone_toasts_text: str,
    ):
        self.name = name
        self.flag_emote = flag_emote
        self.default_toasts_text = default_toasts_text
        self.special_toasts_text = special_toasts_text
        self.recipient_toasts_text = recipient_toasts_text
        self.gone_toasts_text = gone_toasts_text


languages = [
    ToastLanguage(
        "cs-CZ",
        ":flag_cz:",
        "Toasty číslo",
        "Toasty číslo 69    Naaajssss",
        "Toasty pro ",
        "Toasty došly.",
    ),
    ToastLanguage(
        "sk-SK",
        ":flag_sk:",
        "Tousty číslo",
        "Tousty číslo 69    Naaajssss",
        "Tousty pre ",
        "Tousty sú v piči.",
    ),
    ToastLanguage(
        "en-US",
        ":flag_us:",
        "Toasts number",
        "Toasts number 69    Nice",
        "Toasts for",
        "Toasts are out of stock.",
    ),
]


class Toasts(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot

    def get_language_names():
        names = []
        for lang in languages:
            names.append(lang.name)
        return names

    async def autocomp_language_names(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user_input: str
    ):
        return [
            lang for lang in languages if user_input.lower() in lang.name
        ]

    def get_language_by_name(self, name: str):
        for lang in languages:
            if lang.name == name:
                return lang
        return None

    @commands.slash_command(description="Vyhlásí tousty.")
    async def toasts(
        self,
        inter: disnake.ApplicationCommandInteraction,
        number: int = commands.Param(
            ge=0,
            le=200,
            name="number",
            description="Číslo volaných toustů, 0 = došly",
            default=69
        ),
        recipient: str = commands.Param(
            name="recipient",
            description="Jméno příjemce volaných toustů v 2. pádě (Pro koho? Čeho?)",
            default=None
        ),
        lang: str = commands.Param(
            name="language",
            description="Jazyk pro vyhlášení toustů",
            default="cs-CZ",
            choices=get_language_names()
        )
    ):
        await inter.response.defer()

        # Get language object
        language = self.get_language_by_name(lang)

        # Prepare variables for toasts declaring
        text = ".   "
        if recipient is not None:
            # Recipient way
            logger.info('Going to declare toasts for "%s" in "%s".', recipient, lang)
            full_filename = f"toasts-for-recipient-{number}.{lang}.wav"
            number = -1
            text += f"{language.recipient_toasts_text} {recipient}"
            response_text = f":arrow_right: \"{recipient}\""
        else:
            # Number way
            logger.info('Going to declare toasts %s in "%s".', number, lang)
            full_filename = f"toasts-number-{number}.{lang}.wav"
            text += f"{language.default_toasts_text} {number}"
            response_text = str(number)
            if number == 69:
                text = f".   {language.special_toasts_text}"
                response_text = f"{number} <:nepSmug:827833315822141451>"
            elif number == 0:
                text = f".   {language.gone_toasts_text}"
                response_text = f"{language.gone_toasts_text} <:sadIvo:567039959257710592>"

        # Add flag emote by language to response
        response_text += f" {language.flag_emote}"

        # If file is not in local directory create it
        if not exists(full_filename):
            q = requests.utils.quote(text)
            request = await asyncio.to_thread(
                requests.get,
                f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={q}",
            )
            await asyncio.to_thread(
                Path(f"{Config.toasts_sounds_path}/{full_filename[:-4]}.mp3").write_bytes,
                request.content,
            )

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

        # Send response message to channel
        await inter.followup.send(
            content=f":white_check_mark: :sandwich: {response_text}"
        )
