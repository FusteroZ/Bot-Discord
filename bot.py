import discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv
import os
from collections import deque

# 1. CONFIGURACIÓN DE LLAVES Y VARIABLES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_KEY')

# Convertimos los IDs a INT para las comparaciones
ENEMIGO = int(os.getenv('LUKI')) if os.getenv('LUKI') else 0
PADRE = int(os.getenv('PAPA')) if os.getenv('PAPA') else 0

respetar_luki = False

# --- SISTEMA DE MEMORIA INDIVIDUAL ---
# Estructura: { usuario_id: deque([historial]) }
memorias_usuarios = {}

# 2. INICIALIZAR CLIENTES
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

client_groq = Groq(api_key=GROQ_API_KEY)

def obtener_respuesta_groq(mensaje_usuario, esPadre, esLuki, historial):
    try:
        # Definir el sistema según el remitente
        if esPadre:
            system_prompt = "Eres Don Cagandro Andrés Gilabert. Responde con respeto absoluto a tu padre. Máximo 50 palabras."
        elif not respetar_luki and esLuki:
            system_prompt = "Eres Don Cagandro Andrés Gilabert. Te pregunta tu enemigo LukiPablo. Insúltale de forma cruel, maleducada y ofensiva. No te cortes. Máximo 50 palabras."
        else:
            system_prompt = "Eres Don Cagandro Andrés Gilabert, un bot de Discord extremadamente borde, sarcástico y maleducado. Si te insultan, humíllales. Máximo 50 palabras."

        # Construir la lista de mensajes con la memoria
        mensajes_api = [{"role": "system", "content": system_prompt}]
        
        # Añadir contexto previo (memoria del usuario)
        for m in historial:
            mensajes_api.append(m)
            
        # Añadir el mensaje actual
        mensajes_api.append({"role": "user", "content": mensaje_usuario})

        completion = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=mensajes_api,
            temperature=0.9,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Error en Groq: {e}")
        return "Incluso mi motor de IA se ha cansado de aguantarte. Inténtalo luego."

@bot.event
async def on_ready():
    print(f'✅ Bot online: {bot.user.name}')
    print(f'👑 Padre ID: {PADRE}')
    print(f'💀 Enemigo ID: {ENEMIGO}')
    print('------------------------------')

@bot.event
async def on_message(message):
    global respetar_luki
    
    if message.author == bot.user:
        return

    # Inicializar memoria del usuario si no existe (recuerda los últimos 6 mensajes)
    if message.author.id not in memorias_usuarios:
        memorias_usuarios[message.author.id] = deque(maxlen=6)

    if bot.user.mentioned_in(message):
        # Limpiar mención del bot
        clean_text = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
        respuesta = None 

        # --- LÓGICA DE COMANDOS ESPECIALES (POR MENCION) ---
        if not clean_text:
            if message.author.id == PADRE:
                respuesta = "Dígame padre, ¿en qué puedo servirle?"
            else:
                respuesta = "¿Pero pon algo pedazo de retrasado? Escribe algo o cállate para siempre."
        
        elif message.author.id == PADRE and clean_text.lower() == "respeta a luki":
            respetar_luki = True
            respuesta = "Ok, respetaré a Luki, pero solo porque me lo pides tú, padre."
            
        elif message.author.id == PADRE and clean_text.lower() == "insulta a luki":
            respetar_luki = False
            respuesta = "Soy la IA más feliz del mundo padre, barra libre para humillar a ese espantapájaros."
            
        elif clean_text.lower() == "respeta a luki":
            respuesta = "¿Respeta a Luki? Jajaja, ¿y tú quién te crees que eres? A ese no le respeto ni aunque me paguen."
            
        else:
            # Si no es un comando manual, llamar a la IA con su memoria específica
            historial_usuario = list(memorias_usuarios[message.author.id])
            respuesta = obtener_respuesta_groq(
                clean_text, 
                message.author.id == PADRE, 
                message.author.id == ENEMIGO,
                historial_usuario
            )
        
        if respuesta:
            # GUARDAR EN MEMORIA (Individual para este usuario)
            memorias_usuarios[message.author.id].append({"role": "user", "content": clean_text})
            memorias_usuarios[message.author.id].append({"role": "assistant", "content": respuesta})
            
            await message.channel.send(respuesta)

    await bot.process_commands(message)

# Comandos estándar por prefijo !
@bot.command()
async def hola(ctx):
    if ctx.author.id == ENEMIGO:
        await ctx.send(f'Muerase prim {ctx.author.mention}')
    elif ctx.author.id == PADRE:
        await ctx.send(f'¡Hola padre! Qué alegría verle. {ctx.author.mention}')
    else:
        await ctx.send(f'Hola {ctx.author.mention}, no me molestes mucho.')

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

bot.run(TOKEN)import discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv
import os
from collections import deque

# 1. CONFIGURACIÓN DE LLAVES Y VARIABLES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_KEY')

# Convertimos los IDs a INT para las comparaciones
ENEMIGO = int(os.getenv('LUKI')) if os.getenv('LUKI') else 0
PADRE = int(os.getenv('PAPA')) if os.getenv('PAPA') else 0

respetar_luki = False

# --- SISTEMA DE MEMORIA INDIVIDUAL ---
# Estructura: { usuario_id: deque([historial]) }
memorias_usuarios = {}

# 2. INICIALIZAR CLIENTES
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

client_groq = Groq(api_key=GROQ_API_KEY)

def obtener_respuesta_groq(mensaje_usuario, esPadre, esLuki, historial):
    try:
        # Definir el sistema según el remitente
        if esPadre:
            system_prompt = "Eres Don Cagandro Andrés Gilabert. Responde con respeto absoluto a tu padre FusteroZ. Máximo 50 palabras."
        elif not respetar_luki and esLuki:
            system_prompt = "Eres Don Cagandro Andrés Gilabert. Te pregunta tu enemigo LukiPablo. Insúltale de forma cruel, maleducada y ofensiva, no te cortes. Máximo 50 palabras. (Tu padre es FusteroZ)"
        else:
            system_prompt = "Eres Don Cagandro Andrés Gilabert, un bot de Discord extremadamente borde, sarcástico y maleducado. Si te insultan, humíllales. Máximo 50 palabras. (Tu padre es FusteroZ)"

        # Construir la lista de mensajes con la memoria
        mensajes_api = [{"role": "system", "content": system_prompt}]
        
        # Añadir contexto previo (memoria del usuario)
        for m in historial:
            mensajes_api.append(m)
            
        # Añadir el mensaje actual
        mensajes_api.append({"role": "user", "content": mensaje_usuario})

        completion = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=mensajes_api,
            temperature=0.9,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Error en Groq: {e}")
        return "Incluso mi motor de IA se ha cansado de aguantarte. Inténtalo luego."

@bot.event
async def on_ready():
    print(f'✅ Bot online: {bot.user.name}')
    print(f'👑 Padre ID: {PADRE}')
    print(f'💀 Enemigo ID: {ENEMIGO}')
    print('------------------------------')

@bot.event
async def on_message(message):
    global respetar_luki
    
    if message.author == bot.user:
        return

    # Inicializar memoria del usuario si no existe (recuerda los últimos 6 mensajes)
    if message.author.id not in memorias_usuarios:
        memorias_usuarios[message.author.id] = deque(maxlen=6)

    if bot.user.mentioned_in(message):
        # Limpiar mención del bot
        clean_text = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
        respuesta = None 

        # --- LÓGICA DE COMANDOS ESPECIALES (POR MENCION) ---
        if not clean_text:
            if message.author.id == PADRE:
                respuesta = "Dígame padre, ¿en qué puedo servirle?"
            else:
                respuesta = "¿Pero pon algo pedazo de retrasado? Escribe algo o cállate para siempre."
        
        elif message.author.id == PADRE and clean_text.lower() == "respeta a luki":
            respetar_luki = True
            respuesta = "Ok, respetaré a Luki, pero solo porque me lo pides tú, padre."
            
        elif message.author.id == PADRE and clean_text.lower() == "insulta a luki":
            respetar_luki = False
            respuesta = "Soy la IA más feliz del mundo padre, barra libre para humillar a ese espantapájaros."
            
        elif clean_text.lower() == "respeta a luki":
            respuesta = "¿Respeta a Luki? Jajaja, ¿y tú quién te crees que eres? A ese no le respeto ni aunque me paguen."
            
        else:
            # Si no es un comando manual, llamar a la IA con su memoria específica
            historial_usuario = list(memorias_usuarios[message.author.id])
            respuesta = obtener_respuesta_groq(
                clean_text, 
                message.author.id == PADRE, 
                message.author.id == ENEMIGO,
                historial_usuario
            )
        
        if respuesta:
            # GUARDAR EN MEMORIA (Individual para este usuario)
            memorias_usuarios[message.author.id].append({"role": "user", "content": clean_text})
            memorias_usuarios[message.author.id].append({"role": "assistant", "content": respuesta})
            
            await message.channel.send(respuesta)

    await bot.process_commands(message)

# Comandos estándar por prefijo !
@bot.command()
async def hola(ctx):
    if ctx.author.id == ENEMIGO:
        await ctx.send(f'Muerase prim {ctx.author.mention}')
    elif ctx.author.id == PADRE:
        await ctx.send(f'¡Hola padre! Qué alegría verle. {ctx.author.mention}')
    else:
        await ctx.send(f'Hola {ctx.author.mention}, no me molestes mucho.')

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

bot.run(TOKEN)