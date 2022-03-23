import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config


class Spotify():
    def __init__(
        self
    ):
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyOAuth(
                client_id=Config.spotify_client_id,
                client_secret=Config.spotify_client_secret,
                redirect_uri=Config.spotify_redirect_uri,
                scope=Config.spotify_scope
            )
        )

    def stop_playback_if_playing(
        self
    ):
        current_playback = self.spotify.current_playback()
        if current_playback != None:
            if current_playback["is_playing"]:
                self.spotify.pause_playback()
                return True
        return False

    def start_playback_if_stopped(
        self
    ):
        current_playback = self.spotify.current_playback()
        if current_playback != None:
            if not current_playback["is_playing"]:
                self.spotify.start_playback()
                return True
        return False
