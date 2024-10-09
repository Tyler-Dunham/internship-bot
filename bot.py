import os
import discord
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from job import job
from utils import get_cron_times

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = int(os.getenv('CHANNEL_ID'))
testing = os.getenv('TESTING', 'False').lower() in ('true', '1', 't')

# dumb windows problem where it needs different loop policy
import asyncio
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = intents=discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    scheduler.start()

async def send_internships():
    channel = client.get_channel(CHANNEL)
    if channel is None:
        print(f"Invalid channel id {CHANNEL}")
        return

    internships = job()
    for key, internship in internships.items():
        if 'New York, NY' in internship['location'] or 'Remote' in internship['location']:
            message = (
            f"Company: {internship['company']}\n"
            f"Position: {internship['position']}\n"
            f"Locations: {internship['location']}\n"
            f"URL: <{internship['url']}>\n"
            f"Apply lazy ass bitch - <@250087120306307073>"
            f"----------------------------------"
            )
        else:
            message = (
            f"Company: {internship['company']}\n"
            f"Position: {internship['position']}\n"
            f"Locations: {internship['location']}\n"
            f"URL: <{internship['url']}>\n"
            f"----------------------------------"
            )
        await channel.send(message)
    print("Sent internships")

scheduler = AsyncIOScheduler()
cron = get_cron_times(testing=testing)
scheduler.add_job(send_internships, 'cron', hour=cron['hour'], minute=cron['minute'])

client.run(TOKEN)