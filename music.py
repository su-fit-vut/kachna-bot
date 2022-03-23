import disnake
from disnake.ext import commands
from config import Config
from pygame import mixer
import datetime
import helper
import logging
from spotify import Spotify
import time


class Music(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot
        self._last_member = None
        self.spotify = Spotify()

        logging.info("Creating sound object")
        self.sound = mixer.Sound(Config.sound_path)
        self.wait_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=Config.wait_time)

    async def autocomp_songs(
        inter: disnake.ApplicationCommandInteraction,
        user_input: str
    ):
        sounds_names = []
        for sound in Config.sounds:
            sounds_names.append(sound.name)
        return [sound for sound in sounds_names if user_input.lower() in sound]

    @commands.slash_command(description="Přehaj krátký zvuk v Kachně.")
    async def play(
        self,
        inter: disnake.ApplicationCommandInteraction,
        sound: str = commands.Param(name="sound", autocomplete=autocomp_songs)
    ):
        """Play short sound in student club"""
        # Send response message
        await inter.response.send_message(":thinking: :musical_note:")

        # Find sound
        sounds_names = ""
        for sound_from_config in Config.sounds:
            sounds_names += f"- {sound_from_config.name}\n"
            if sound.lower() == sound_from_config.name.lower():
                # update message
                await inter.edit_original_message(
                    content=str(sound_from_config.emote)
                )

                # Spotify pause playback
                self.spotify.stop_playback_if_playing()

                # play found sound
                sound_from_config.play()

                # Wait until sound is playing
                time.sleep(5)

                # Spotify start playback
                self.spotify.start_playback_if_stopped()

                return

        # send message when sound is not found
        await inter.edit_original_message(
            content=f"Tento zvuk ještě neumím zahrát, zkus něco z těchto:\n{sounds_names[:-1]}"
        )

    @commands.slash_command()
    async def spotify(
        self,
        inter: disnake.ApplicationCommandInteraction,
    ):
        pass

    @spotify.sub_command_group()
    async def queue(
        self,
        inter: disnake.ApplicationCommandInteraction,
    ):
        pass

    @queue.sub_command(description="Přidat písničku do Spotify fronty.")
    async def add(
        self,
        inter: disnake.ApplicationCommandInteraction,
        track_id: str = commands.Param(name="song_url")
    ):
        """
        Parameters
        ----------
        track_id: ID skladby na Spotify
        """
        # Send response message
        await inter.response.send_message(":thinking: :heavy_plus_sign: :musical_note:")

        self.spotify.spotify.add_to_queue(track_id)
        track = self.spotify.spotify.track(track_id)
        embed = disnake.Embed(
            title="Skladba přidána do fronty. :white_check_mark:",
            description=f"Písnička \"{track['name']}\" byla úspěšně zařazena na konec fronty.",
            color=0x1DB954
        )
        embed.set_thumbnail(url=track["album"]["images"][0]["url"])

        # Update message
        await inter.edit_original_message(
            content="",
            embed=embed
        )
