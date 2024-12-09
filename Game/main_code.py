from multiprocessing import process
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv  
import os  


load_dotenv()

CHANNEL_ID = 1313869335822864435 


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


if len(sys.argv) < 3:
    print("Fehlende Argumente: logfile und username erwartet.")
    sys.exit(1)

logfile = sys.argv[1]
username = sys.argv[2]

@bot.event
async def on_ready():
    print(f"Bot ist eingeloggt als {bot.user}")

  
    try:
        with open(logfile, 'r', encoding='utf-8', errors='replace') as f:
            logs = f.read()
    except FileNotFoundError:
        print("Log-Datei nicht gefunden!")
        logs = "Keine Logs verfügbar."

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"Neue Logs hochgeladen von {username}:\n```{logs}```")
        print("Nachricht erfolgreich gesendet!")
    else:
        print("Channel nicht gefunden!")

bot_token = os.getenv("TOKEN")
if bot_token is None:
    print("Token nicht gefunden! Bitte überprüfe die .env-Datei.")
    sys.exit(1)

bot.run(bot_token)
