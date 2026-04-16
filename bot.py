import discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv
import os

# 1. CONFIGURACIÓN DE LLAVES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_KEY')
ENEMIGO = os.getenv('LUKI')
PADRE = os.getenv('PAPA')
respetar_luki = False

# 2. INICIALIZAR CLIENTES
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

client_groq = Groq(api_key=GROQ_API_KEY)

# Función para obtener respuesta de Groq
def obtener_respuesta_groq(mensaje_usuario, esPadre, esLuki):
    try:
        if(esPadre):
            completion = client_groq.chat.completions.create(
                # MODELO ACTUALIZADO: llama-3.3-70b-versatile es mucho más inteligente y está activo
                model="llama-3.3-70b-versatile", 
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres Don Cagandro Andrés Gilabert, un bot de Discord. Responde con respeto como si te hubiese preguntado tu padre. Si no lo ves necesario no te pases de 50 palabras"
                    },
                    {
                        "role": "user", 
                        "content": mensaje_usuario
                    }
                ],
                temperature=0.9,
                max_tokens=150
            )
            return completion.choices[0].message.content
        elif not respetar_luki and esLuki:
            completion = client_groq.chat.completions.create(
                # MODELO ACTUALIZADO: llama-3.3-70b-versatile es mucho más inteligente y está activo
                model="llama-3.3-70b-versatile", 
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres Don Cagandro Andrés Gilabert, un bot de Discord mal educado. Te esta preguntando LukiPablo, tu peor enemigo, insultale de la peor forma que se te ocurra con menos de 50 palabras. No te cortes, sé lo más ofensivo posible."
                    },
                    {
                        "role": "user", 
                        "content": mensaje_usuario
                    }
                ],
                temperature=0.9,
                max_tokens=150
            )
            return completion.choices[0].message.content
        else:
            completion = client_groq.chat.completions.create(
                # MODELO ACTUALIZADO: llama-3.3-70b-versatile es mucho más inteligente y está activo
                model="llama-3.3-70b-versatile", 
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres Don Cagandro Andrés Gilabert, un bot de Discord mal educado. Si la gente te pregunta algo de buena forma respondes con un poco de sarcasmo, pero si te insultan o te molestan, les insultas de la peor forma que se te ocurra con menos de 50 palabras. No te cortes, sé lo más ofensivo posible."
                    },
                    {
                        "role": "user", 
                        "content": mensaje_usuario
                    }
                ],
                temperature=0.9,
                max_tokens=150
            )
            return completion.choices[0].message.content
    except Exception as e:
        # Si por algún motivo el 70b falla, prueba con "llama-3.1-8b-instant"
        print(f"❌ Error en Groq: {e}")
        return "Hasta mi motor de IA se ha cansado de aguantarte. Inténtalo luego."
    
@bot.event
async def on_ready():
    print(f'✅ Bot online: {bot.user.name}')
    print('Utilizando motor: Groq (Llama 3)')

@bot.event
async def on_message(message):
    responder = False

    if message.author == bot.user:
        return

    # Si mencionan al bot
    if bot.user.mentioned_in(message):
        print(f'📩 Mensaje de {message.author}: {message.content}')
        
        # Limpiar mención
        clean_text = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
        
        if not clean_text and message.author.id == PADRE:
            clean_text = "Padre hablame por favor, no me ignores :("
        elif not clean_text:
            clean_text = "¿Pero pon algo pedazo de retrasado? Mira que eres más retardado que el modelo de 70b sin optimizar, escribe algo o cállate para siempre."
        elif message.author.id == PADRE and clean_text.lower() == "respeta a luki":
            clean_text = "Ok, respetaré a Luki, pero solo porque me lo pides tu, no porque me importe un carajo ese retrasado mental de mierda."
            respetar_luki = True
        elif message.author.id == PADRE and clean_text.lower() == "insulta a luki":
            clean_text = "Soy la IA más feliz del mundo padre"
            respetar_luki = False
        elif clean_text.lower() == "respeta a luki":
            clean_text = "¿Respeta a Luki? Jajajaja, ¿y por qué debería respetar a ese retrasado mental de mierda? Ni siquiera es digno de mi atención, así que no lo respetaré ni aunque me lo pidas por favor."
        else:
            responder = True 

        # Obtener respuesta de la IA
        if(responder):
            respuesta = obtener_respuesta_groq(clean_text, message.author.id == PADRE, message.author.id == ENEMIGO)
        
        if respuesta:
            await message.channel.send(respuesta)

    await bot.process_commands(message)

# Comandos clásicos
@bot.command()
async def hola(ctx):
    if ctx.author.id == ENEMIGO:
        await ctx.send(f'Muerase prim {ctx.author.mention}')
    elif ctx.author.id == PADRE:
        await ctx.send(f'¡Hola padre! {ctx.author.mention}')
    else:
        await ctx.send(f'Hola {ctx.author.mention}, no me molestes mucho.')

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

# Ejecutar
bot.run(TOKEN)