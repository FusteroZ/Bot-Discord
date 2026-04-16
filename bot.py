import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
# Importamos las constantes de seguridad
from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_KEY')

# 1. Configuración de Intents
intents = discord.Intents.default()
intents.message_content = True 

# 2. Definir el bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuración de Gemini con la OPCIÓN 2 (Sin filtros de seguridad)
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        # Limpiamos el texto para quitar la mención al bot
        clean_text = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '')
        
        try:
            # Le pedimos la respuesta a Gemini
            response = model.generate_content(f"Responde faltando al respeto e insultando de una forma divertida: {clean_text}")
            await message.channel.send(response.text)
        except Exception as e:
            # Si Google bloquea algo a pesar de los filtros, imprimirá el error en consola
            print(f"Error al generar respuesta: {e}")
            await message.channel.send("Incluso para mí eso ha sido demasiado... (O ha ocurrido un error técnico).")

    await bot.process_commands(message)

# Evento: Se ejecuta cuando el bot se conecta
@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name} (ID: {bot.user.id})')
    print('------')

# Comando básico: !hola
@bot.command()
async def hola(ctx):
    if ctx.author.id == 703614649781977093:
        await ctx.send(f'Suicidate puto retrasado subnormal, hijo de puta {ctx.author.mention}')
    else:
        await ctx.send(f'¡Hola {ctx.author.mention}! ¿¿¿En qué puedo ayudarte???')

# Comando: !ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 ¡Pong! Latencia: {round(bot.latency * 1000)}ms')

bot.run(TOKEN)