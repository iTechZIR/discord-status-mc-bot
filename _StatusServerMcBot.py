import discord
from discord.ext import commands
from discord import app_commands
from mcstatus import JavaServer
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        return
    
    await joinvoice()
    bot.loop.create_task(updatebotstatus()) 

async def joinvoice():
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if channel.name == "namevoisechanel":
                try:
                    await channel.connect()
                    return
                except Exception as e:
                    return

async def updatebotstatus():
    server = JavaServer.lookup("ip")  
    laststatus = None  

    while True:
        try:
            status = server.status()
            player_count = status.players.online
            mainstatus = f"{player_count} Players"
        except Exception:
            mainstatus = "Server Offline ❌"

        if mainstatus != laststatus:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=mainstatus))
            laststatus = mainstatus

        await asyncio.sleep(10)

bot.run('Token')
