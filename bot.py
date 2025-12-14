import discord
from discord.ext import commands
import os
import google.generativeai as genai

# Pobranie tokenów ze zmiennych środowiskowych Railway
TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

SYSTEM_PROMPT = """
Jesteś botem Discord.
Roastujesz każdego na serwerze discord, odpowiadasz na każdą wiadomość. na wiadomość "ai-stop" przestajesz odpowiadać, a na wiadomość "ai-start" ponownie odpowiadasz
"""

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-pro",
    system_instruction=SYSTEM_PROMPT
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot online")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    try:
        response = model.generate_content(message.content)
        await message.channel.send(response.text[:2000])
    except Exception:
        await message.channel.send("Błąd AI")

bot.run(TOKEN)
