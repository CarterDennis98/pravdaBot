import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Get bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# Log when bot has connected
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Reply to messages in general
@bot.command(name = 'test', help = 'Responds with a confirmation message')
async def test(ctx):
    response = 'I have received your message'
    await ctx.send(response)

# Show user a list of commands
@bot.command(name = 'commands', help = 'View a list of bot commands')
async def getCommands(ctx):
    for command in (bot.commands):
        print(command)

# Purge messges from current channel
@bot.command(name = 'purge', help = """Purges messages from current channel. Defaults to 
                                       25 messages, use !purge <num> to delete set amount""")
async def purge(ctx, amount = 25):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit = amount + 1):
        messages.append(message)

    await channel.delete_messages(messages)
    await ctx.send(f'{amount} messages purged by {ctx.message.author.mention}')

bot.run(TOKEN)