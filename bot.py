import discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv
import os

# 1. CONFIGURACIÓN DE LLAVES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_KEY')

# Convertimos los IDs a INT para que las comparaciones funcionen
ENEMIGO = int(os.getenv('LUKI')) if os.getenv('LUKI') else 0
PADRE = int(os.getenv('PAPA')) if os.getenv('PAPA') else 0

respetar_luki = False

# 2. INICIALIZAR CLIENTES
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

client_groq = Groq(api_key=GROQ_API_KEY)

def obtener_respuesta_groq(mensaje_usuario, esPadre, esLuki):
    try:
        # Lógica de sistema según quién pregunta
        if esPadre:
            system_prompt = "Eres Don Cagandro Andrés Gilabert. Responde con respeto absoluto a tu padre. Máximo 50 palabras."
        elif not respetar_luki and esLuki:
            system_prompt = "Eres Don Cagandro Andrés Gilabert. Te pregunta tu enemigo LukiPablo. Insúltale de forma cruel y ofensiva. Máximo 50 palabras."
        else:
            system_prompt = "Eres Don Cagandro Andrés Gilabert, un bot borde y sarcástico. Si te insultan, sé muy ofensivo. Máximo 50 palabras."

        completion = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje_usuario}
            ],
            temperature=0.9,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Error en Groq: {e}")
        return "Hasta mi motor de IA se ha cansado de aguantarte."
    
@bot.event
async def on_ready():
    print(f'✅ Bot online: {bot.user.name}')

@bot.event
async def on_message(message):
    global respetar_luki # IMPORTANTE: Para poder modificar la variable de arriba
    
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        clean_text = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
        respuesta = None # Inicializamos para evitar errores

        # Lógica de comandos especiales por mención
        if not clean_text:
            if message.author.id == PADRE:
                respuesta = "Dígame padre, ¿en qué puedo servirle?"
            else:
                respuesta = "¿Pero pon algo pedazo de retrasado? Escribe algo o cállate."
        
        elif message.author.id == PADRE and clean_text.lower() == "respeta a luki":
            respetar_luki = True
            respuesta = "Ok, respetaré a Luki, pero solo porque me lo pides tú."
            
        elif message.author.id == PADRE and clean_text.lower() == "insulta a luki":
            respetar_luki = False
            respuesta = "Soy la IA más feliz del mundo padre, barra libre para humillar a ese espantapájaros."
            
        elif clean_text.lower() == "respeta a luki":
            respuesta = "¿Respeta a Luki? ¿Tú quién te crees? A ese no le respeto ni aunque me paguen."
            
        else:
            # Si no es un comando especial, preguntamos a la IA
            respuesta = obtener_respuesta_groq(clean_text, message.author.id == PADRE, message.author.id == ENEMIGO)
        
        if respuesta:
            await message.channel.send(respuesta)

    await bot.process_commands(message)

@bot.command()
async def hola(ctx):
    if ctx.author.id == ENEMIGO:
        await ctx.send(f'Muerase prim {ctx.author.mention}')
    elif ctx.author.id == PADRE:
        await ctx.send(f'¡Hola padre! {ctx.author.mention}')
    else:
        await ctx.send(f'Hola {ctx.author.mention}, no me molestes.')

bot.run(TOKEN)