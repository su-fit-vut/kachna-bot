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
    def __init__(self, bot):
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
        for s in Config.sounds:
            sounds_names.append(s.name)
        return [sound for sound in sounds_names if user_input.lower() in sound]
    
    @commands.slash_command(description="Přehaj krátký zvuk v Kachně.")
    async def play(
        self,
        inter: disnake.ApplicationCommandInteraction,
        sound: str = commands.Param(name="sound", autocomplete=autocomp_songs)
        ):
        """Play short sound in student club"""
        
        sounds_names = ""
        for s in Config.sounds:
            sounds_names += f"- {s.name}\n"
            if sound.lower() == s.name.lower():
                await inter.response.send_message(str(s.emote))
                return s.play()
        
        await inter.response.send_message(f"Tento zvuk ještě neumím zahrát, zkus něco z těchto:\n{sounds_names[:-1]}")

    @commands.slash_command(description="Přidat písničku do Spotify fronty.")
    async def add_to_queue(
        self,
        inter: disnake.ApplicationCommandInteraction,
        track_id: str = commands.Param(name="song_url")
        ):
        """Add song to queue"""

        self.spotify.add_to_queue(track_id)
        t = self.spotify.track(track_id)
        e = disnake.Embed(
            title = "Song queued. ✅",
            description = f"Successfully added track \"{t['name']}\" to queue.",
            color = 0x1DB954
            )
        e.set_thumbnail(url=t["album"]["images"][0]["url"])
        
        await inter.response.send_message(embed=e)
