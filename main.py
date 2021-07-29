import os
import asyncio
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

# Show user a list of commands
@bot.command(name = 'commands', help = 'View a list of bot commands')
async def getCommands(ctx):
    for command in (bot.commands):
        print(command)

# Purge messges from current channel
@bot.command(name = 'purge', help = """Purges messages from current channel. Defaults to 
                                       25 messages, use !purge [num] to delete set amount
                                       or !purge all to clear entire channel.""")
async def purge(ctx, amount = None):
    user = ctx.message.author
    print(user)
    if amount is None:
        numMsg = 0
        async for msg in ctx.channel.history(limit = None):
            numMsg += 1
        await ctx.channel.purge(limit = 21)
        numMsg -= 1
        await ctx.send(f'{numMsg} message(s) purged by {ctx.message.author.mention}', delete_after = 5)
    elif amount == 'all':
        msg = await ctx.send(f'Are you sure you want to clear all messages in this channel (#{ctx.channel})?')
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        def check(reaction, user):
            return str(reaction.emoji) == '✅' and user != bot.user

        try:
            reaction, user = await bot.wait_for('reaction_add', check=check)
            await ctx.send(f'{user} cleared channel successfully')
        except asyncio.TimeoutError:
            await ctx.send("You ran out of time to decide!")
        #await ctx.channel.purge()
        #await ctx.send(f'All messages purged by {ctx.message.author.mention}', delete_after = 5)
    else:
        await ctx.channel.purge(limit = int(amount) + 1)
        await ctx.send(f'{amount} message(s) purged by {ctx.message.author.mention}', delete_after = 5)

bot.run(TOKEN)