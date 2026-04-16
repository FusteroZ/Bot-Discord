import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 1. Configuración de Intents (Permisos)
# Esto permite que el bot lea mensajes y vea quién está en el servidor
# Configuración correcta de Intents
intents = discord.Intents.default()
intents.message_content = True  # Esto permite que el bot lea tus mensajes

# 2. Definir el prefijo del bot (ejemplo: !hola, !ping)
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento: Se ejecuta cuando el bot se conecta
@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name} (ID: {bot.user.id})')
    print('------')

# Comando básico: !hola
@bot.command()
async def hola(ctx):
    if ctx.author.id == 703614649781977093:
        await ctx.send(f'Suicidate puto retrasado subnormal, hijo de puta {ctx.author.mention}')  # Ignorar mensajes de otros bots
    else:
        await ctx.send(f'¡Hola {ctx.author.mention}! ¿En qué puedo ayudarte?')

# Comando: !ping (para ver la latencia)
@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 ¡Pong! Latencia: {round(bot.latency * 1000)}ms')

bot.run(TOKEN)