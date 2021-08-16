import os
import datetime
import asyncio
import discord
from discord import file
from discord.ext import commands

# Get bot token
TOKEN = os.environ["TOKEN"]

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
@commands.has_any_role('Admin', 'Leader', 'Officer', 'master')
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
                                generate headcount for exaltation dungeons (!hc [exaltation]), or
                                generate rune check (!hc [runes]""")
async def hc(ctx, dungeon='all'):
    await ctx.channel.purge(limit=1)
    dungeon = dungeon.lower()
    if(dungeon == 'exaltations'):
        embed = discord.Embed(title=f'Headcount for Exaltation Dungeons', color=discord.Color.blue(),
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
    elif(dungeon == 'o3' or dungeon == 'oryx 3' or dungeon == 'oryx3'):
        embed = discord.Embed(title='Headcount for Oryx 3', color=discord.Color.from_rgb(235,214,110),
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
        await msg.add_reaction('<:knight:874140434203570216>')
        await msg.add_reaction('<:warrior:874140400695250974>')
        await msg.add_reaction('<:paladin:874140420760817685>')
        await msg.add_reaction('<:priest:874141506011807805>')
        await msg.add_reaction('<:slow:874141187592822784>')
        await msg.add_reaction('<:armorBreak:874141141744881694>')
        await msg.add_reaction('<:curse:874141153811922966>')
        await msg.add_reaction('<:daze:874141162200526848>')
        await msg.add_reaction('<:expose:874141172442992690>')
    elif(dungeon == 'shatters'):
        embed = discord.Embed(title='Headcount for The Shatters', color=discord.Color.from_rgb(59,62,59),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for The Shatters started by {ctx.message.author.name}!',
                        value='React with <:shattersPortal:874068565559488522> to join or with <:shattersKey:874070162574311504> if you have keys you want to pop.')
        img = discord.File('images/forgottenKing.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:shattersPortal:874068565559488522>')
        await msg.add_reaction('<:shattersKey:874070162574311504>')
        await msg.add_reaction('<:knight:874140434203570216>')
        await msg.add_reaction('<:warrior:874140400695250974>')
        await msg.add_reaction('<:paladin:874140420760817685>')
        await msg.add_reaction('<:priest:874141506011807805>')
        await msg.add_reaction('<:slow:874141187592822784>')
        await msg.add_reaction('<:armorBreak:874141141744881694>')
        await msg.add_reaction('<:curse:874141153811922966>')
        await msg.add_reaction('<:daze:874141162200526848>')
        await msg.add_reaction('<:expose:874141172442992690>')
    elif(dungeon == 'nest'):
        embed = discord.Embed(title='Headcount for The Nest', color=discord.Color.from_rgb(231,121,28),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for The Nest started by {ctx.message.author.name}!',
                        value='React with <:nestPortal:874068640708853810> to join or with <:nestKey:874070151685898292> if you have keys you want to pop.')
        img = discord.File('images/queenBee.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:nestPortal:874068640708853810>')
        await msg.add_reaction('<:nestKey:874070151685898292>')
        await msg.add_reaction('<:knight:874140434203570216>')
        await msg.add_reaction('<:warrior:874140400695250974>')
        await msg.add_reaction('<:paladin:874140420760817685>')
        await msg.add_reaction('<:priest:874141506011807805>')
        await msg.add_reaction('<:slow:874141187592822784>')
        await msg.add_reaction('<:armorBreak:874141141744881694>')
        await msg.add_reaction('<:curse:874141153811922966>')
        await msg.add_reaction('<:daze:874141162200526848>')
        await msg.add_reaction('<:expose:874141172442992690>')
    elif(dungeon == 'fungal'):
        embed = discord.Embed(title='Headcount for Fungal Cavern', color=discord.Color.from_rgb(189,46,206),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for Fungal Cavern started by {ctx.message.author.name}!',
                        value='React with <:fungalPortal:874068627098337320> to join or with <:fungalKey:874070120132124684> if you have keys you want to pop.')
        img = discord.File('images/crystalMother.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:fungalPortal:874068627098337320>')
        await msg.add_reaction('<:fungalKey:874070120132124684>')
        await msg.add_reaction('<:knight:874140434203570216>')
        await msg.add_reaction('<:warrior:874140400695250974>')
        await msg.add_reaction('<:paladin:874140420760817685>')
        await msg.add_reaction('<:priest:874141506011807805>')
        await msg.add_reaction('<:slow:874141187592822784>')
        await msg.add_reaction('<:armorBreak:874141141744881694>')
        await msg.add_reaction('<:curse:874141153811922966>')
        await msg.add_reaction('<:daze:874141162200526848>')
        await msg.add_reaction('<:expose:874141172442992690>')
    elif(dungeon == 'cult'):
        embed = discord.Embed(title='Headcount for Cultist Hideout', color=discord.Color.from_rgb(155,25,26),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for Cultist Hideout started by {ctx.message.author.name}!',
                        value='React with <:cultPortal:874068612032368640> to join or with <:hallsKey:874070141170749470> if you have keys you want to pop.')
        img = discord.File('images/malus.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:cultPortal:874068612032368640>')
        await msg.add_reaction('<:hallsKey:874070141170749470>')
        await msg.add_reaction('<:knight:874140434203570216>')
        await msg.add_reaction('<:warrior:874140400695250974>')
        await msg.add_reaction('<:paladin:874140420760817685>')
        await msg.add_reaction('<:priest:874141506011807805>')
        await msg.add_reaction('<:slow:874141187592822784>')
        await msg.add_reaction('<:armorBreak:874141141744881694>')
        await msg.add_reaction('<:curse:874141153811922966>')
        await msg.add_reaction('<:daze:874141162200526848>')
        await msg.add_reaction('<:expose:874141172442992690>')
    elif(dungeon == 'void' or dungeon == 'the void'):
        embed = discord.Embed(title='Headcount for The Void', color=discord.Color.from_rgb(27,4,110),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for The Void started by {ctx.message.author.name}!',
                        value='React with <:voidPortal:874068593422262373> to join, <:hallsKey:874070141170749470> if you have keys you want to pop, or <:vial:874140033593004082> if you are bringing vial.')
        img = discord.File('images/void.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        msg = await ctx.send(file=img, embed=embed)
        await msg.add_reaction('<:voidPortal:874068593422262373>')
        await msg.add_reaction('<:hallsKey:874070141170749470>')
        await msg.add_reaction('<:vial:874140033593004082>')
        await msg.add_reaction('<:knight:874140434203570216>')
        await msg.add_reaction('<:warrior:874140400695250974>')
        await msg.add_reaction('<:paladin:874140420760817685>')
        await msg.add_reaction('<:priest:874141506011807805>')
        await msg.add_reaction('<:slow:874141187592822784>')
        await msg.add_reaction('<:armorBreak:874141141744881694>')
        await msg.add_reaction('<:curse:874141153811922966>')
        await msg.add_reaction('<:daze:874141162200526848>')
        await msg.add_reaction('<:expose:874141172442992690>')
    elif(dungeon == 'pcave' or dungeon == 'pirate cave' or dungeon == 'forest maze' or dungeon == 'sden'
         or dungeon == 'spider den' or dungeon == 'snake pit' or dungeon == 'fjungle' or dungeon == 'forbidden jungle'
         or dungeon == 'hive' or dungeon == 'mwoods' or dungeon == 'magic woods' or dungeon == 'sprite'
         or dungeon == 'sprite world' or dungeon == 'cland' or dungeon == 'candyland' or dungeon == 'ruins'
         or dungeon == 'ancient ruins' or dungeon == 'tcave' or dungeon == 'coatt' or dungeon == 'udl'
         or dungeon == 'undead lair' or dungeon == 'abyss' or dungeon == 'abyss of demons' or dungeon == 'manor'
         or dungeon == 'puppet' or dungeon == 'sewers' or dungeon == 'library' or dungeon == 'cursed library'
         or dungeon == 'cem' or dungeon == 'cemetery' or dungeon == 'haunted cem' or dungeon == 'haunted cemetery'
         or dungeon == 'machine' or dungeon == 'the machine' or dungeon == 'lab' or dungeon == 'mad lab'
         or dungeon == 'mlab' or dungeon == 'ddocks' or dungeon == 'deadwater docks' or dungeon == 'wlab'
         or dungeon == 'woodlab' or dungeon == 'woodland labyrinth' or dungeon == 'cdepths' or dungeon == 'cd'
         or dungeon == 'crawling depths' or dungeon == 'parasite' or dungeon == 'para' or dungeon == 'beachzone'
         or dungeon == '3d' or dungeon == 'third dimension' or dungeon == 'davy jones' or dungeon == 'davy'
         or dungeon == 'mt' or dungeon == 'mountain temple' or dungeon == 'lod' or dungeon == 'lair of draconis'
         or dungeon == 'ot' or dungeon == 'trench' or dungeon == 'ocean trench' or dungeon == 'ice cave'
         or dungeon == 'tomb' or dungeon == 'malogia' or dungeon == 'red' or dungeon == 'red alien'
         or dungeon == 'untaris' or dungeon == 'blue' or dungeon == 'blue alien' or dungeon == 'forax'
         or dungeon == 'green' or dungeon == 'green alien' or dungeon == 'katalund' or dungeon == 'yellow'
         or dungeon == 'yellow alien' or dungeon == 'shaitan' or dungeon == 'pup encore' or dungeon == 'encore'
         or dungeon == 'puppet encore' or dungeon == 'reef' or dungeon == 'cnidarian reef' or dungeon == 'thicket'
         or dungeon == 'htt' or dungeon == 'hudl' or dungeon == 'heroic udl' or dungeon == 'habyss'
         or dungeon == 'heroic abyss' or dungeon == 'bnex' or dungeon == 'bnexus' or dungeon == 'battle nexus' 
         or dungeon == 'bella' or dungeon == 'bellas' or dungeon == 'belladonna' or dungeon == 'ice tomb'
         or dungeon == 'rainbow' or dungeon == 'rainbow road' or dungeon == 'mgm' or dungeon == 'mad god mayhem'):
        if(dungeon == 'pcave' or dungeon == 'pirate cave'):
            dungeon = 'Pirate Cave'
            thumb = discord.File('images/dreadstump.png', filename='image.png')
            dColor = discord.Color.from_rgb(159,93,69)
        elif(dungeon == 'forest maze'):
            dungeon = 'Forest Maze'
            thumb = discord.File('images/mamaMegamoth.png', filename='image.png')
            dColor = discord.Color.from_rgb(86,125,0)
        elif(dungeon == 'sden' or dungeon == 'spider den'):
            dungeon = 'Spider Den'
            thumb = discord.File('images/arachna.png', filename='image.png')
            dColor = discord.Color.from_rgb(87,122,67)
        elif(dungeon == 'snake pit'):
            dungeon = 'Snake Pit'
            thumb = discord.File('images/stheno.png', filename='image.png')
            dColor = discord.Color.from_rgb(81,166,80)
        elif(dungeon == 'fjungle' or dungeon == 'forbidden jungle'):
            dungeon = 'Forbidden Jungle'
            thumb = discord.File('images/mixcoatl.png', filename='image.png')
            dColor = discord.Color.from_rgb(140,35,205)
        elif(dungeon == 'hive'):
            dungeon = 'The Hive'
            thumb = discord.File('images/queenBeeHive.png', filename='image.png')
            dColor = discord.Color.from_rgb(251,198,65)
        elif(dungeon == 'mwoods' or dungeon == 'magic woods'):
            dungeon = 'Magic Woods'
            thumb = discord.File('images/fountainSpirit.png', filename='image.png')
            dColor = discord.Color.from_rgb(128,202,241)
        elif(dungeon == 'sprite' or dungeon == 'sprite world'):
            dungeon = 'Sprite World'
            thumb = discord.File('images/limon.png', filename='image.png')
            dColor = discord.Color.from_rgb(192,58,49)
        elif(dungeon == 'cland' or dungeon == 'candyland'):
            dungeon = 'Candyland Hunting Grounds'
            thumb = discord.File('images/gigacorn.png', filename='image.png')
            dColor = discord.Color.from_rgb(225,146,199)
        elif(dungeon == 'ruins' or dungeon == 'ancient ruins'):
            dungeon = 'Ancient Ruins'
            thumb = discord.File('images/sandstoneTitan.png', filename='image.png')
            dColor = discord.Color.from_rgb(205,177,107)
        elif(dungeon == 'tcave' or dungeon == 'coatt'):
            dungeon = 'Cave of a Thousand Treasures'
            thumb = discord.File('images/goldenOryx.png', filename='image.png')
            dColor = discord.Color.from_rgb(231,209,16)
        elif(dungeon == 'udl' or dungeon == 'undead lair'):
            dungeon = 'Undead Lair'
            thumb = discord.File('images/septavius.png', filename='image.png')
            dColor = discord.Color.from_rgb(102,112,145)
        elif(dungeon == 'abyss' or dungeon == 'abyss of demons'):
            dungeon = 'Abyss of Demons'
            thumb = discord.File('images/malphas.png', filename='image.png')
            dColor = discord.Color.from_rgb(162,34,37)
        elif(dungeon == 'manor'):
            dungeon = 'Manor of the Immortals'
            thumb = discord.File('images/ruthven.png', filename='image.png')
            dColor = discord.Color.from_rgb(72,65,105)
        elif(dungeon == 'puppet'):
            dungeon = 'Puppet Master\'s Theatre'
            thumb = discord.File('images/puppetMaster.png', filename='image.png')
            dColor = discord.Color.from_rgb(164,4,5)
        elif(dungeon == 'sewers'):
            dungeon = 'Toxic Sewers'
            thumb = discord.File('images/gulpord.png', filename='image.png')
            dColor = discord.Color.from_rgb(83,74,22)
        elif(dungeon == 'library' or dungeon == 'cursed library'):
            dungeon = 'Cursed Library'
            thumb = discord.File('images/avalon.png', filename='image.png')
            dColor = discord.Color.from_rgb(55,62,102)
        elif(dungeon == 'cem' or dungeon == 'cemetery' or dungeon == 'haunted cem' or dungeon == 'haunted cemetery'):
            dungeon = 'Haunted Cemetery'
            thumb = discord.File('images/skuld.png', filename='image.png')
            dColor = discord.Color.from_rgb(51,98,73)
        elif(dungeon == 'machine' or dungeon == 'the machine'):
            dungeon = 'The Machine'
            thumb = discord.File('images/null.png', filename='image.png')
            dColor = discord.Color.from_rgb(88,158,26)
        elif(dungeon == 'lab' or dungeon == 'mlab' or dungeon == 'mad lab'):
            dungeon = 'Mad Lab'
            thumb = discord.File('images/drTerrible.png', filename='image.png')
            dColor = discord.Color.from_rgb(10,120,225)
        elif(dungeon == 'ddocks' or dungeon == 'deadwater docks'):
            dungeon = 'Deadwater Docks'
            thumb = discord.File('images/bilgewater.png', filename='image.png')
            dColor = discord.Color.from_rgb(152,33,65)
        elif(dungeon == 'wlab' or dungeon == 'woodlab' or dungeon == 'woodland labyrinth'):
            dungeon = 'Woodland Labyrinth'
            thumb = discord.File('images/murderousMegamoth.png', filename='image.png')
            dColor = discord.Color.from_rgb(224,113,62)
        elif(dungeon == 'cd' or dungeon == 'cdepths' or dungeon == 'crawling depths'):
            dungeon = 'Crawling Depths'
            thumb = discord.File('images/arachnaSon.png', filename='image.png')
            dColor = discord.Color.from_rgb(24,39,34)
        elif(dungeon == 'parasite' or dungeon == 'para'):
            dungeon = 'Parasite Chambers'
            thumb = discord.File('images/nightmareColony.png', filename='image.png')
            dColor = discord.Color.from_rgb(211,95,97)
        elif(dungeon == 'beachzone'):
            dungeon = 'Beachzone'
            thumb = discord.File('images/partyGod.png', filename='image.png')
            dColor = discord.Color.from_rgb(221,180,108)
        elif(dungeon == '3d' or dungeon == 'third dimension'):
            dungeon = 'The Third Dimension'
            thumb = discord.File('images/tesseract.png', filename='image.png')
            dColor = discord.Color.from_rgb(146,184,222)
        elif(dungeon == 'davy' or dungeon == 'davy jones'):
            dungeon = 'Davy Jones\' Locker'
            thumb = discord.File('images/davyJones.png', filename='image.png')
            dColor = discord.Color.from_rgb(54,46,92)
        elif(dungeon == 'mt' or dungeon == 'mountain temple'):
            dungeon = 'Mountain Temple'
            thumb = discord.File('images/daichi.png', filename='image.png')
            dColor = discord.Color.from_rgb(82,14,4)
        elif(dungeon == 'lod' or dungeon == 'lair of draconis'):
            dungeon = 'Lair of Draconis'
            thumb = discord.File('images/ivoryWyvern.png', filename='image.png')
            dColor = discord.Color.from_rgb(210,173,32)
        elif(dungeon == 'ot' or dungeon == 'trench' or dungeon == 'ocean trench'):
            dungeon = 'Ocean Trench'
            thumb = discord.File('images/thessal.png', filename='image.png')
            dColor = discord.Color.from_rgb(11,98,213)
        elif(dungeon == 'ice cave'):
            dungeon = 'Ice Cave'
            thumb = discord.File('images/esben.png', filename='image.png')
            dColor = discord.Color.from_rgb(115,199,255)
        elif(dungeon == 'tomb'):
            dungeon = 'Tomb of the Ancients'
            thumb = discord.File('images/geb.png', filename='image.png')
            dColor = discord.Color.from_rgb(225,200,117)
        elif(dungeon == 'malogia' or dungeon == 'red' or dungeon == 'red alien'):
            dungeon = 'Malogia'
            thumb = discord.File('images/suesogian.png', filename='image.png')
            dColor = discord.Color.from_rgb(176,77,84)
        elif(dungeon == 'untaris' or dungeon == 'blue' or dungeon == 'blue alien'):
            dungeon = 'Untaris'
            thumb = discord.File('images/tarul.png', filename='image.png')
            dColor = discord.Color.from_rgb(64,116,185)
        elif(dungeon == 'forax' or dungeon == 'green' or dungeon == 'green alien'):
            dungeon = 'Forax'
            thumb = discord.File('images/acidus.png', filename='image.png')
            dColor = discord.Color.from_rgb(22,115,71)
        elif(dungeon == 'katalund' or dungeon == 'yellow' or dungeon == 'yellow alien'):
            dungeon = 'Katalund'
            thumb = discord.File('images/goldenSphinx.png', filename='image.png')
            dColor = discord.Color.from_rgb(220,173,16)
        elif(dungeon == 'shaitan'):
            dungeon = 'Lair of Shaitan'
            thumb = discord.File('images/shaitan.png', filename='image.png')
            dColor = discord.Color.from_rgb(210,23,8)
        elif(dungeon == 'encore' or dungeon == 'pup encore' or dungeon == 'puppet encore'):
            dungeon = 'Puppet Master\'s Encore'
            thumb = discord.File('images/puppetMasterEncore.png', filename='image.png')
            dColor = discord.Color.from_rgb(67,65,87)
        elif(dungeon == 'reef' or dungeon == 'cnidarian reef'):
            dungeon = 'Cnidarian Reef'
            thumb = discord.File('images/royalCnidarian.png', filename='image.png')
            dColor = discord.Color.from_rgb(245,165,77)
        elif(dungeon == 'thicket'):
            dungeon = 'Secluded Thicket'
            thumb = discord.File('images/xolotl.png', filename='image.png')
            dColor = discord.Color.from_rgb(131,173,35)
        elif(dungeon == 'htt'):
            dungeon = 'High Tech Terror'
            thumb = discord.File('images/feral.png', filename='image.png')
            dColor = discord.Color.from_rgb(7,120,233)
        elif(dungeon == 'hudl' or dungeon == 'heroic udl'):
            dungeon = 'Heroic Undead Lair'
            thumb = discord.File('images/heroicSeptavius.png', filename='image.png')
            dColor = discord.Color.from_rgb(232,171,39)
        elif(dungeon == 'habyss' or dungeon == 'heroic abyss'):
            dungeon = 'Heroic Abyss of Demons'
            thumb = discord.File('images/heroicMalphas.png', filename='image.png')
            dColor = discord.Color.from_rgb(232,171,39)
        elif(dungeon == 'bnex' or dungeon == 'bnexus' or dungeon == 'battle nexus'):
            dungeon = 'Battle for the Nexus'
            thumb = discord.File('images/oryxDeux.png', filename='image.png')
            dColor = discord.Color.from_rgb(148,16,13)
        elif(dungeon == 'bella' or dungeon == 'bellas' or dungeon == 'belladonna'):
            dungeon = 'Belladonna\'s Garden'
            thumb = discord.File('images/belladonna.png', filename='image.png')
            dColor = discord.Color.from_rgb(235,137,160)
        elif(dungeon == 'ice tomb'):
            dungeon = 'Ice Tomb'
            thumb = discord.File('images/iceShard.png', filename='image.png')
            dColor = discord.Color.from_rgb(157,244,234)
        elif(dungeon == 'rainbow' or dungeon == 'rainbow road'):
            dungeon = 'Rainbow Road'
            thumb = discord.File('images/potOfGold.png', filename='image.png')
            dColor = discord.Color.from_rgb(28,195,44)
        elif(dungeon == 'mgm' or dungeon == 'mad god mayhem'):
            dungeon = 'Mad God Mayhem'
            thumb = discord.File('images/decaract.png', filename='image.png')
            dColor = discord.Color.from_rgb(244,0,10)

        embed = discord.Embed(title=f'Headcount for {dungeon}', color=dColor, timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f'Headcount for {dungeon} started by {ctx.message.author.name}!',
                        value='React with <:dungeonPortal:874070478128562236> to join or with <:dungeonKey:874070489163776060> if you have keys you want to pop.')
        embed.set_thumbnail(url=f'attachment://image.png')
        msg = await ctx.send(file=thumb, embed=embed)
        await msg.add_reaction('<:dungeonPortal:874070478128562236>')
        await msg.add_reaction('<:dungeonKey:874070489163776060>')

bot.run(TOKEN)