import os
import discord
from dotenv import load_dotenv
import schedule
import time
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL_ID')

#dumb windows problem where it needs different loop policy
import asyncio
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = intents=discord.Intents.default()
client = discord.Client(intents=intents)

def job():
    parsed_internships = []
    commits = get_commits()
    for commit in commits:
        commit_data = get_commit(commit['sha'])
        parsed_commit = parse_commit(commit_data)
        parsed_internships.append(parsed_commit)


def get_commits():
    url = "https://api.github.com/repos/username/repo/commits"
    response = requests.get(url)
    return response.json()

def get_commit(sha: str):
    url = f"https://api.github.com/repos/username/repo/commits/{sha}"
    response = requests.get(url)
    return response.json()

def parse_commit(commit):
    return {}

schedule.every(5).seconds.do(job)
#schedule.every(1).day.at("00:00").do(job) 

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def send_internships():
    channel = client.get_channel()
    job()

client.run(TOKEN)
while True:
    schedule.run_pending()
    time.sleep(1)