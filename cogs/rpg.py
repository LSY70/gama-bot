import discord
from discord import app_commands
from discord.ext import commands
from cogs.tools.rpg_systems import Cellbit

class RPG(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name='desconjuração', description="Rola dados no sistema de Desconjuração")
    async def opd(self, interaction: discord.Interaction, pericia: int, dado: int = 20):
        from random import randint
        from Imagens import imagem
        name = f'{interaction.user.name}'
        valor = randint(1, dado)
        prc = rst = ''
        nome = f'Nome: {name}'
        if pericia:
            resul = Cellbit().OPD(v=valor, p=pericia)
            prc = f'Pericia: {pericia}'
            rst = f'Resultado: {resul}'
        imagem.imagens_pericia(nome=nome, valor=str(valor), pericia=prc, resultado=rst)
        await interaction.response.send_message(file=discord.File(r'Imagens/resultado.png'))
    
    async def dano(self, ctx: commands.Context, dado: str, x: int):
        res = Cellbit().OPC(dado, x=x)
        card = discord.Embed(color=discord.Color.from_rgb(255, 0, 0))
        card.add_field(name='Rolagem completa' if not 'Erro' in res else "Rolagem inválida", value=res,
                        inline=False)
        card.set_footer(text=ctx.author.nick, icon_url=ctx.author.avatar)
        await ctx.send(embed=card)
    
    @app_commands.command(name='calamidade', description="Rola dados no sistema de Calamidade")
    async def opc(self, interaction: discord.Interaction, dado: str):
        ctx = await self.bot.get_context(interaction)
        await self.dano(ctx=ctx, dado=dado, x=1)

    @app_commands.command(name='dano', description="Rola dados de dano")
    async def dano_dado(self, interaction: discord.Interaction, dado: str):
        ctx = await self.bot.get_context(interaction)
        await self.dano(ctx=ctx, dado=dado, x=0)

async def setup(bot):
    await bot.add_cog(RPG(bot))
