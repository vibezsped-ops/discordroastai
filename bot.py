import discord
from discord.ext import commands
import os
import google.generativeai as genai
from dotenv import load_dotenv

# ładowanie zmiennych ze .env
load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

SYSTEM_PROMPT = """
Jesteś botem Discord.
Odpowiadasz naturalnie, krótko i na temat.
Nie moralizujesz ani nie oceniasz.
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
