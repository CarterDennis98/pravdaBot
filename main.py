import os

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
                                       25 messages, use !purge <num> to delete set amount
                                       or !purge all to clear entire channel.""")
async def purge(ctx, amount = None):
    if amount is None:
        numMsg = 0
        async for msg in ctx.channel.history(limit = None):
            numMsg += 1
        await ctx.channel.purge(limit = 26)
        numMsg -= 1
        await ctx.send(f'{numMsg} message(s) purged by {ctx.message.author.mention}', delete_after = 5)
    elif amount == "all":
        await ctx.channel.purge()
        await ctx.send(f'All messages purged by {ctx.message.author.mention}', delete_after = 5)
    else:
        await ctx.channel.purge(limit = int(amount) + 1)
        await ctx.send(f'{amount} message(s) purged by {ctx.message.author.mention}', delete_after = 5)

bot.run(TOKEN)