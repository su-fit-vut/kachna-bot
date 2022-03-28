from playsound import playsound
import logging
import time


class Sound():
    def __init__(
        self,
        name,
        files,
        spotify,
        emote=None
    ):
        self.name = name
        self.files = files
        self.emote = (emote if emote != None else "☑️")
        self.spotify = spotify

    def play(
        self
    ):
        logging.info(f"Playing sound \"{self.name}\"")
        for file in self.files:
            playsound(file)

    def play_fade_out(
        self
    ):
        """
        Play sound with fade in and fade out.
        """

        current_playback = self.spotify.current_playback()
        if current_playback == None:
            self.play()
            return
        if current_playback["device"] == None:
            self.play()
            return
        if current_playback["device"]["volume_percent"] == None:
            self.play()
            return
        volume = current_playback["device"]["volume_percent"]

        logging.info("Fade in")
        for i in range(volume, 10, -8):
            self.spotify.volume(i)
            time.sleep(0.250)

        self.play()

        logging.info("Fade out")
        for i in range(10, volume, 8):
            self.spotify.volume(i)
            time.sleep(0.250)
        self.spotify.volume(volume)
        return
