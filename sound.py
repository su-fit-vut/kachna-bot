from playsound import playsound
import time
from spotify import Spotify


class Sound():
    def __init__(
        self,
        name,
        files,
        emote=None
    ):
        self.name = name
        self.files = files
        self.emote = (emote if emote != None else "☑️")
        self.spotify = spotipy.Spotify()

    def play(
        self
    ):
        for file in self.files:
            playsound(file)

    def play_fade_out(
        self
    ):
        """
        Play sound with fade in and fade out.
        """

        current_playback = self.spotify.current_playback()
        print(current_playback)

        for i in range(asdf):
            # Spotify volume
            self.spotify.spotify.volume(10)
            time.sleep(0.250)

        self.play()
        self.spotify.spotify.volume(100)
