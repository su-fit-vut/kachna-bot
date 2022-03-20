from pygame import mixer
import time
import json

class Sound():
    def __init__(self, name, files, emote=None, schedule=None):
        self.name = name
        self.files = files
        self.emote = (emote if emote != None else "☑️")
        self.schedule = schedule
        mixer.init()
        self.ch = mixer.Channel(0)

    async def react_on_message(self, message):
        return await message.add_reaction(self.emote)
    
    async def play_and_react(self, message):
        self.play()
        await self.react_on_message(message)

    def play(self):
        for s in self.files:
            while self.ch.get_queue():
                time.sleep(1)
            self.ch.queue(mixer.Sound(s))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
