import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Get bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

# Log when bot has connected
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Reply to messages in general
@bot.command(name = 'test', help = 'Responds with a confirmation message')
async def test(ctx):
    response = 'I have received your message'
    await ctx.send(response)

client.run(TOKEN)