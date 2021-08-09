import os
import datetime
import asyncio
import discord
from discord import file
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
    embed = discord.Embed(title='Commands', color=discord.Color.green())
    for command in (bot.commands):
        if str(command) == 'help':
            embed.add_field(
                name='!help:', value='Use !help [command] to see how to use the command')
        else:
            embed.add_field(name=f'!{str(command)}:',
                            value=f'{str(command.help)}')
    await ctx.send(embed=embed)

# Purge messges from current channel
@bot.command(name='purge', help="""Purges messages from current channel. Defaults to 
                                   20 messages, use !purge [amount] to delete set amount
                                   or !purge all to clear entire channel.""")
async def purge(ctx, amount=''):
    # Get number of messages in the channel
    numMsg = 0
    async for msg in ctx.channel.history(limit=None):
        numMsg += 1
    if amount == '':
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
    await ctx.channel.purge(limit=1)
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
        poll = discord.Embed(title=f'{title}', color=discord.Color.red(
        ), timestamp=datetime.datetime.utcnow())
        poll.add_field(name='✅', value='Yes')
        poll.add_field(name='❌', value='No')
        msg = await ctx.send(embed=poll)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
    else:
        poll = discord.Embed(title=f'{title}', color=discord.Color.red(
        ), timestamp=datetime.datetime.utcnow())
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        i = 0
        for option in options:
            poll.add_field(name=reactions[i], value=option, inline=False)
            i += 1
        msg = await ctx.send(embed=poll)

        i = 0
        while i < len(options):
            await msg.add_reaction(reactions[i])
            i += 1

# Key headcount/interest check
@bot.command(name='hc', help="""Set up a headcount for the desire dungeon with !hc ["dungone name"], 
                                generate headcount for exaltation dungeons (!hc [exaltation]),
                                generate rune check (!hc [runes], or generate headcount for all dungeons (!hc)""")
async def hc(ctx, dungeon='all'):
    await ctx.channel.purge(limit=1)
    if(dungeon == 'exaltations'):
        embed = discord.Embed(title='Headcount for Exaltation Dungeons', color=discord.Color.blue(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount started for Exaltation Dungeons by {ctx.message.author.name}!',
                        value='React with any keys you are willing to pop or react with the corresponding portal if you wish to participate.')
        img = discord.File('images/exaltedWizard.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:shattersPortal:874068565559488522>')
        await msg.add_reaction('<:shattersKey:874070162574311504>')
        await msg.add_reaction('<:nestPortal:874068640708853810>')
        await msg.add_reaction('<:nestKey:874070151685898292>')
        await msg.add_reaction('<:fungalPortal:874068627098337320>')
        await msg.add_reaction('<:fungalKey:874070120132124684>')
        await msg.add_reaction('<:cultPortal:874068612032368640>')
        await msg.add_reaction('<:voidPortal:874068593422262373>')
        await msg.add_reaction('<:hallsKey:874070141170749470>')
    elif(dungeon == 'o3' or dungeon == 'O3' or dungeon == 'Oryx 3'):
        embed = discord.Embed(title='Headcount for Oryx 3', color=discord.Color.blue(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for Oryx 3 started by {ctx.message.author.name}!',
                        value='React with <:osancPortal:874068648115982438> to participate or with <:shieldRune:874070197949071402> <:helmetRune:874070181675163658> <:swordRune:874070189141004429> <:inc:874079430002221077> if you have runes/inc you want to pop.')
        img = discord.File('images/o3.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:osancPortal:874068648115982438>')
        await msg.add_reaction('<:shieldRune:874070197949071402>')
        await msg.add_reaction('<:helmetRune:874070181675163658>')
        await msg.add_reaction('<:swordRune:874070189141004429>')
        await msg.add_reaction('<:inc:874079430002221077>')
    elif(dungeon == 'shatters' or dungeon == 'Shatters'):
        embed = discord.Embed(title='Headcount for The Shatters', color=discord.Color.blue(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for The Shatters started by {ctx.message.author.name}!',
                        value='React with <:shattersPortal:874068565559488522> to join or with <:shattersKey:874070162574311504> if you have keys you want to pop.')
        img = discord.File('images/forgottenKing.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:shattersPortal:874068565559488522>')
        await msg.add_reaction('<:shattersKey:874070162574311504>')
    elif(dungeon == 'nest' or dungeon == 'Nest'):
        embed = discord.Embed(title='Headcount for The Nest', color=discord.Color.blue(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for The Nest started by {ctx.message.author.name}!',
                        value='React with <:nestPortal:874068640708853810> to join or with <:nestKey:874070151685898292> if you have keys you want to pop.')
        img = discord.File('images/queenBee.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:nestPortal:874068640708853810>')
        await msg.add_reaction('<:nestKey:874070151685898292>')
    elif(dungeon == 'fungal' or dungeon == 'Fungal'):
        embed = discord.Embed(title='Headcount for Fungal Cavern', color=discord.Color.blue(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for Fungal Cavern started by {ctx.message.author.name}!',
                        value='React with <:fungalPortal:874068627098337320> to join or with <:fungalKey:874070120132124684> if you have keys you want to pop.')
        img = discord.File('images/crystalMother.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:fungalPortal:874068627098337320>')
        await msg.add_reaction('<:fungalKey:874070120132124684>')
    elif(dungeon == 'cult' or dungeon == 'Cult'):
        embed = discord.Embed(title='Headcount for Cultist Hideout', color=discord.Color.blue(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for Cultist Hideout started by {ctx.message.author.name}!',
                        value='React with <:cultPortal:874068612032368640> to join or with <:hallsKey:874070141170749470> if you have keys you want to pop.')
        img = discord.File('images/malus.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:cultPortal:874068612032368640>')
        await msg.add_reaction('<:hallsKey:874070141170749470>')
    elif(dungeon == 'void' or dungeon == 'Void'):
        embed = discord.Embed(title='Headcount for The Void', color=discord.Color.blue(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for The Void started by {ctx.message.author.name}!',
                        value='React with <:voidPortal:874068593422262373> to join or with <:hallsKey:874070141170749470> if you have keys you want to pop.')
        img = discord.File('images/void.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:voidPortal:874068593422262373>')
        await msg.add_reaction('<:hallsKey:874070141170749470>')


bot.run(TOKEN)
