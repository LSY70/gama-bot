import discord
from discord import app_commands
from discord.ext import commands

queues = {}
historic = {}
loop = {}
tocando = {}

def check_queue(ctx, guild, init=True):
    if init and queues[guild]:
        source = queues[guild].pop(0)
        historic[guild].append(source)
        if len(historic[guild]) > 10:
            historic[guild].pop(0)
        if loop[guild]:
            queues[guild].append(source)
    if queues[guild]:
        ffmpeg = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        client_voice = ctx.voice_client
        source = queues[guild][0].get_audio()
        client_voice.play(discord.FFmpegOpusAudio(source, **ffmpeg), after=lambda x: check_queue(ctx, guild))
        client_voice.is_playing()

def add_button(label, callback, style=discord.ButtonStyle.grey, Button=discord.ui.Button):
    button = Button(label=label, style=style)
    button.callback = callback
    return button

def verifica(self):
    if not self.member_voice or not self.member_voice.channel:
        return None
    if not self.ctx.voice_client:
        return None
    if self.member_voice.channel != self.ctx.voice_client.channel:
        return None
    if self.client_voice.is_playing():
        return True
    else:
        return False

class MusicButtons(discord.ui.View):
    def __init__(self, bot: commands.Bot, server, ctx: commands.Context):
        super().__init__(timeout=180)
        self.bot = bot
        self.server = server
        self.ctx = ctx
        self.member_voice = ctx.author.voice
        self.client_voice = ctx.voice_client
        self.backbutton = add_button(label='⏮️', callback=self.back_button)
        label = '🔂' if loop[server] else '🔁'
        color = discord.ButtonStyle.green if loop[server] else discord.ButtonStyle.grey
        self.loopbutton = add_button(label=label, callback=self.loop_button, style=color)
        self.exitbutton = add_button(label='✖️', callback=self.exit_button, style=discord.ButtonStyle.danger)
        label = '⏸️' if tocando[server] else '▶️'
        color = discord.ButtonStyle.green if tocando[server] else discord.ButtonStyle.grey
        self.playbutton = add_button(label=label, callback=self.play_button, style=color)
        self.skipbutton = add_button(label='⏭️', callback=self.skip_button)
        verificador = verifica(self)
        buttons = [self.backbutton, self.loopbutton, self.exitbutton, self.playbutton, self.skipbutton]
        if verificador:
            for button in buttons:
                self.add_item(button)
        elif verificador != None:
            self.add_item(self.exitbutton)
        else:
            return
    
    async def back_button(self, interaction: discord.Interaction):
        musica = historic[self.server].pop()
        queues[self.server].insert(0, musica)
        queues[self.server].insert(0, musica)
        if verifica(self):
            self.client_voice.stop()
            await interaction.response.edit_message(view=self)

    async def play_button(self,interaction: discord.Interaction):
        verif = verifica(self)
        if verif:
            self.playbutton.style=discord.ButtonStyle.grey
            self.playbutton.label = '▶️'
            self.client_voice.pause()
        elif verif == False:
            self.playbutton.style=discord.ButtonStyle.green
            self.playbutton.label = '⏸️'
            self.client_voice.resume()
        if verif != None:
            tocando[self.server] = self.client_voice.is_playing()
            await interaction.response.edit_message(view=self)

    async def skip_button(self, interaction: discord.Interaction):
        if verifica(self):
            self.client_voice.stop()
            await interaction.response.edit_message(view=self)

    async def exit_button(self, interaction: discord.Interaction):
        if verifica(self) != None:
            try:
                if self.ctx.voice_client.is_playing():
                    self.ctx.voice_client.stop()
                queues[self.server] = []
                historic[self.server] = []
                await self.ctx.voice_client.disconnect()
                await self.ctx.send("Desconectado com sucesso!", ephemeral=True)
            except Exception as error:
                await self.ctx.send('Erro ao desconectar-se', ephemeral=True)
            await interaction.response.edit_message(view=self)

    async def loop_button(self, interaction: discord.Interaction):
        if loop[self.server]:
            loop[self.server] = False
            self.loopbutton.label = "🔁"
            self.loopbutton.style=discord.ButtonStyle.grey
        else:
            loop[self.server] = True
            self.loopbutton.label = "🔂"
            self.loopbutton.style=discord.ButtonStyle.green
        await interaction.response.edit_message(view=self)
        await self.ctx.send(content='Loop ativado!' if loop[self.server] else 'Loop desativado!', ephemeral=True)


class Musicas(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        voice_client = member.guild.voice_client
        if voice_client:
            if voice_client.channel == before.channel:
                if len(member.guild._voice_states[894263121521311835].channel.members) == 1:
                    queues[member.guild.id] = []
                    historic[member.guild.id] = []
                    loop[member.guild.id] = False
                    await voice_client.disconnect()
    
    async def connect_call_command(self, interaction):
        ctx = await self.bot.get_context(interaction)
        member_voice = ctx.author.voice
        if member_voice and member_voice.channel:
            if not ctx.voice_client:
                await member_voice.channel.connect()
                await interaction.edit_original_response(content="Conectado.")
        else:
            await interaction.edit_original_response(content="Entre em um canal de voz para usar este comando.")
    
    @app_commands.command(name="controle", description="Controle de musica")
    async def music_controler(self, interaction: discord.Interaction) -> None:
        ctx = await self.bot.get_context(interaction)
        server = interaction.guild.id
        if verifica != None:
            title = queues[server][0].get_info()["Titulo"] if queues[server] else "Sem musicar por aqui..."
        else:
            title = "Sem musicas por aqui..."
        await interaction.response.send_message(content=title, view=(MusicButtons(bot=self.bot, server=server, ctx=ctx)), ephemeral=True)

    @app_commands.command(name="connect", description="Entrar na chamada")
    async def connect_call(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(content="Conectando...", ephemeral=True)
        await self.connect_call_command(interaction=interaction)

    @app_commands.command(name="play", description="Adiciona uma musica à lista")
    async def add_music(self, interaction: discord.Interaction, *, musica: str, only_view: bool = False) -> None:
        from cogs.tools.search import Youtube
        await interaction.response.send_message(content="Buscando...", ephemeral=only_view)
        video = Youtube(musica)
        info = video.get_info()
        await interaction.edit_original_response(content=f"Encontrada: [{info['Titulo']}]")
        ctx = await self.bot.get_context(interaction)
        card = discord.Embed()
        server = ctx.message.guild.id
        if server not in list(loop.keys()):
            loop[server] = False
        if server not in list(historic.keys()):
            historic[server] = []
        if server not in list(tocando.keys()):
            tocando[server] = True
        await self.connect_call_command(interaction=interaction)
        if ctx.voice_client:
            client_voice = ctx.voice_client
            if client_voice.is_playing():
                    card = discord.Embed(title="Adicionado a lista", color=discord.Color.from_rgb(255, 0, 0))
                    if server in queues:
                        queues[server].append(video)
                    else:
                        queues[server] = [video]
            else:
                card = discord.Embed(color=discord.Color.from_rgb(255, 0, 0))
                queues[server] = [video]
                check_queue(ctx, server, init=False)
            info_r = f'```css\nTempo: {info["Time"]//60}m {info["Time"]%60}s\nViews: {info["Views"]}\nCanal: {info["Canal"]}\n```'
            card.add_field(name=info["Titulo"], value=info_r)
            card.set_image(url=info["Thumbnail"])
            await interaction.edit_original_response(content=None, embed=card)
    
    @app_commands.command(name='queue', description="Mostra a lista de musicas adicionadas")
    async def queue(self, interaction: discord.Interaction):
        card = discord.Embed(title='LISTA DE MUSICAS GAMABOT', color=discord.Color.from_rgb(255, 0, 0))
        self.ctx = await self.bot.get_context(interaction)
        self.server = self.ctx.message.guild.id
        self.member_voice = self.ctx.author.voice
        self.client_voice = self.ctx.voice_client
        if verifica(self) != None:
            c = 0
            for item in queues[self.server]:
                info = item.get_info()
                time = int(info["Time"])
                tempo = f'{time//60}:{0 if time%60 < 10 else ""}{time%60}'
                value = str(f'```\n{info["Canal"]} | {tempo} | {info["Views"]} views\n```')
                if c == 0:
                    card.add_field(name=f'►{info["Titulo"]}', value=value, inline=False, )
                else:
                    card.add_field(name=f'  {info["Titulo"]}', value=value,  inline=False,)
                if c == 5:
                    card.add_field(name=f'5 de {len(queues[self.server])}', value='max range list', inline=False)
                    break
                c += 1
            await self.ctx.send(embed=card)


async def setup(bot):
    await bot.add_cog(Musicas(bot))
