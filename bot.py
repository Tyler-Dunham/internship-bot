import os
import discord
from dotenv import load_dotenv
from cron import job

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#dumb windows problem where it needs different loop policy
import asyncio
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')



client.run(TOKEN)