import os
import discord
from dotenv import load_dotenv
import schedule
import time
from job import job

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL_ID')

#dumb windows problem where it needs different loop policy
import asyncio
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = intents=discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def send_internships():
    channel = client.get_channel(CHANNEL)
    internships = job()
    for internship in internships:
        await channel.send(internship)

client.run(TOKEN)

# Cron every day at midnight
schedule.every(5).seconds.do(send_internships)
while True:
    schedule.run_pending()
    time.sleep(1)