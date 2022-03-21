import disnake
from disnake.ext import commands
from config import Config
from pygame import mixer
import datetime
import helper
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Music(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot
        self._last_member = None

        logging.info("Creating sound object")
        self.sound = mixer.Sound(Config.sound_path)
        self.wait_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=Config.wait_time)
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyOAuth(
                client_id=Config.spotify_client_id,
                client_secret=Config.spotify_client_secret,
                redirect_uri=Config.spotify_redirect_uri,
                scope=Config.spotify_scope
            )
        )
    
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
        
        sounds_names = ""
        for sound_from_config in Config.sounds:
            sounds_names += f"- {sound.name}\n"
            if sound.lower() == sound_from_config.name.lower():
                await inter.response.send_message(str(sound_from_config.emote))
                return sound_from_config.play()
        
        await inter.response.send_message(f"Tento zvuk ještě neumím zahrát, zkus něco z těchto:\n{sounds_names[:-1]}")

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

        self.spotify.add_to_queue(track_id)
        track = self.spotify.track(track_id)
        embed = disnake.Embed(
            title = "Skladba přidána do fronty. ✅",
            description = f"Písnička \"{track['name']}\" byla úspěšně zařazena na konec fronty.",
            color = 0x1DB954
            )
        embed.set_thumbnail(url=track["album"]["images"][0]["url"])
        
        await inter.response.send_message(embed=embed)
