import discord
from discord import app_commands
from discord.ext import commands


class Extras(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name='clear', description="Limpa as mensagens do chat")
    async def cls(self, interaction: discord.Interaction, quantidade: int=500):
        ctx = await self.bot.get_context(interaction)
        await ctx.channel.purge(limit=quantidade)
        await ctx.send(content="Apagando mensagens...", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Extras(bot))
