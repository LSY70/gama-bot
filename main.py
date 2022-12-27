import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')
GUILD = 0


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="./",
            intents=discord.Intents.all()
        )

    async def load(self):
        cogs = os.listdir('cogs')
        for item in cogs:
            if item.endswith('.py'):
                await self.load_extension(f'cogs.{item[:-3]}')
                print(item, 'Carregado')

    async def setup_hook(self):
        await self.load()
        self.tree.copy_global_to(guild=discord.Object(id=GUILD))
        await self.tree.sync()


TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()
client = Bot()
client.run(TOKEN, log_handler=None)
