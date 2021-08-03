import os
import asyncio
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

# Show user a list of commands
@bot.command(name='commands', help='View a list of bot commands')
async def getCommands(ctx):
    for command in (bot.commands):
        print(command)

# Purge messges from current channel
@bot.command(name='purge', help="""Purges messages from current channel. Defaults to 
                                       20 messages, use !purge [amount] to delete set amount
                                       or !purge all to clear entire channel.""")
async def purge(ctx, amount=None):
    # Get number of messages in the channel
    numMsg = 0
    async for msg in ctx.channel.history(limit=None):
        numMsg += 1
    if amount is None:
        # Default purge command, clear up to 20 messages
        await ctx.channel.purge(limit=21)
        numMsg -= 1
        await ctx.send(f'{numMsg} message(s) purged by {ctx.message.author.mention}', delete_after=5)
    elif amount == 'all':
        # Ask user for confirmation they want to clear channel and then clear it
        msg = await ctx.send(f'Are you sure you want to clear all messages in this channel (#{ctx.channel})?')
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        try:
            reaction, user = await bot.wait_for('reaction_add')
            while user == bot.user:
                reaction, user = await bot.wait_for('reaction_add')
            if reaction.emoji == '✅':
                await ctx.channel.purge()
                await ctx.send(f'All messages purged by {ctx.message.author.mention}', delete_after=5)
            if reaction.emoji == '❌':
                await ctx.channel.purge(limit=2)
                await ctx.send(f'That was a close one, {ctx.message.author.mention}!', delete_after=5)
        except Exception:
            return
    else:
        # At most, delete the given amount of messages
        await ctx.channel.purge(limit=int(numMsg) + 1)
        numMsg -= 1
        await ctx.send(f'{numMsg} message(s) purged by {ctx.message.author.mention}', delete_after=5)

# Set up a poll with a set number of choices (1-5) and a set time
@bot.command(name='poll', help="""Set up a poll with 1-5 options. """)
async def poll(ctx, *options: str):
    if len(options) <= 1:
        # If there is 1 or 0 options, tell user input is invalid
        await ctx.send(f'{ctx.message.author.mention}, you must enter more than one option to create a poll!')
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=2)
    elif len(options) > 5:
        # If there are more than 5 options, tell user input is invalid
        await ctx.send(f'{ctx.message.author.mention}, you cannot enter more than 5 options when creating a poll!')
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=2)
    elif len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
        reactions = ['✅', '❌']
        poll = discord.Embed(title='Poll', color=discord.Color.blue())
        poll.add_field(name = f'{options[0]} ✅', value = 'val1')
        poll.add_field(name = f'{options[1]} ❌', value = 'val2')
        msg = await ctx.send(embed = poll)
    else:
        await ctx.send(f'Generate poll with {len(options)} options: {options}')

    # await ctx.author.send(f'I received your poll command with choices: {options}', delete_after = 10)


bot.run(TOKEN)
