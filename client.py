import disnake
from disnake.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__()
