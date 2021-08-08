import os
import datetime
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
    embed=discord.Embed(title='Commands', color=discord.Color.green())
    for command in (bot.commands):
        if str(command) == 'help':
            embed.add_field(name='!help:', value='Use !help [command] to see how to use the command')
        else:
            embed.add_field(name=f'!{str(command)}:', value=f'{str(command.help)}')
    await ctx.send(embed=embed)

# Purge messges from current channel
@bot.command(name='purge', help="""Purges messages from current channel. Defaults to 
                                       20 messages, use !purge [amount] to delete set amount
                                       or !purge all to clear entire channel.""")
async def purge(ctx, amount='0'):
    # Get number of messages in the channel
    numMsg = 0
    async for msg in ctx.channel.history(limit=None):
        numMsg += 1
    if int(amount) == 0:
        # Default purge command, clear up to 20 messages
        await ctx.channel.purge(limit=21)
        numMsg -= 1
        if numMsg > 20:
            await ctx.send(f'20 messages purged by {ctx.message.author.mention}', delete_after=5)
        else:
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
        await ctx.channel.purge(limit=int(amount) + 1)
        numMsg -= 1
        if numMsg > int(amount):
            await ctx.send(f'{amount} message(s) purged by {ctx.message.author.mention}', delete_after=5)
        else:
            await ctx.send(f'{numMsg} message(s) purged by {ctx.message.author.mention}', delete_after=5)

# Set up a poll with a set number of choices (1-5) and a set time
@bot.command(name='poll', help="""Set up a poll with 2-5 options. If no options are given, set up a 
                                  simple Yes/No poll. Format is as follows: !poll [title] [options]
                                  If you want to have spaces in your title/options make sure to put them 
                                  within double ("abc") quotes.""")
async def poll(ctx, title='Poll', *options: str):
    if len(options) <= 1 and len(options) != 0:
        # If there is 1 or negative options, tell user input is invalid
        await ctx.send(f'{ctx.message.author.mention}, you must enter more than one option to create a poll!',
                       delete_after=5)
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=2)
    elif len(options) > 5:
        # If there are more than 5 options, tell user input is invalid
        await ctx.send(f'{ctx.message.author.mention}, you cannot enter more than 5 options when creating a poll!',
                       delete_after=5)
    elif len(options) == 0:
        poll = discord.Embed(title=f'{title}', color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        poll.add_field(name='✅', value='Yes')
        poll.add_field(name='❌', value='No')
        msg = await ctx.send(embed=poll)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
    else:
        await ctx.send(f'Options: {options}')
        poll = discord.Embed(title=f'{title}', color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        i = 0
        for option in options:
            poll.add_field(name=reactions[i], value=option)
            i += 1
        msg = await ctx.send(embed=poll)
        
        i = 0
        while i < len(options):
            await msg.add_reaction(reactions[i])
            i += 1

    # await ctx.author.send(f'I received your poll command with choices: {options}', delete_after = 10)


bot.run(TOKEN)
