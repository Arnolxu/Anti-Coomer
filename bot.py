import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import random as rndm
import funcs
import typing
import string
import time
from PIL import Image, ImageFont, ImageDraw
load_dotenv()
intents = discord.Intents.default()
intents.members= True
intents = discord.Intents.all()
prefix = "ac "
client = commands.Bot(command_prefix=prefix, intents=intents, enale_debug_events=True)
intents.members = True
token = os.getenv("TOKEN")
count = 3
status = True
cogs = ['moderation.py', 'utils.py', 'misc.py']
 
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  lowercase = msg.lower().replace("i̇", "i")
  if f"<@!{client.user.id}>" == lowercase or f"<@{client.user.id}>" == lowercase:
    await message.reply("Prefixim: `" + prefix + "`")
  if "hedef 2023" in lowercase:
    await message.add_reaction("🇧")
    await message.add_reaction("🇴")
    await message.add_reaction("🇷")
  await client.process_commands(message)

@client.event
async def on_ready():
    change_status.start()


@client.command(help='Rastgele Ataturk resimleri atar.')
async def ataturk(ctx):
    global resim_path
    for x in range(1,5):
        resim_path = Image.open(f'AtaturkResimleri/Ata{x}')
    resim = rndm.choice(resim_path)
    await ctx.send(file=resim)


@client.command(help="Kugus Digiligi")
async def kusdili(ctx, mode, *args):
  response = ""
  for arg in args:
    response = response + " " + arg
  response = response[1:len(response)]
  if mode=="tr":
    await ctx.send(funcs.turkDili(response))
  elif mode=="kd":
    await ctx.send(funcs.kusDili(response))
  else:
    await ctx.send("Lütfen düzgün bir mod gir!\norneğin: `k.kusdili kd Merhaba` veya `k.kusdili tr Megerhagabaga` gibi.")

@tasks.loop(seconds=10.0)
async def change_status():
    global count
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1
    if status:
        if(count%3==0):
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=prefix + "help"))
        if(count%3==1):
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Sunucu sayisi: " + str(servers)))
        if(count%3==2):
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Üye sayisi: " + str(members)))
        count = count + 1



@client.command(help="Sadece bot gelistiricisi kullanabilir, botun durumunu degistirir.")
async def status(ctx, *args):
    global status
    if(ctx.author.id==477159179568545795):
        response = ""
        for arg in args:
            response = response + " " + arg
        response = response[1:len(response)]
        if response=="disable":
            status=True
        else:
            status=False
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=response))

@client.command
async def load(ctx, cog):
    client.load_extension(cog)
    await ctx.send('Cog yukleniyor...')
@client.command
async def load(ctx, cog):
    client.unload_extension(cog)
    await ctx.send('Cog devre disi birakiliyor...')

@client.command(help="Kullaniciyi kayit eder.")
async def kayit(ctx):
    if ctx.channel.id != 897191745501155428: # #kayit kanali
        return
    user = ctx.author
    channel = client.get_channel('896686250684207115')
    emojis = ["1️⃣", "2️⃣"]
    secim = await ctx.send('''Merhaba, lutfen politik gorusunu asagidan sec. 
    1️⃣: Muhalif
    2️⃣: Erdoganci''')
    for emoji in emojis:
        await secim.add_reaction(emoji)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != 897191745501155428: # #kayit kanali
        return
    if user == client.user:
        return
    if reaction.emoji == "1️⃣":
        muhalif = discord.utils.get(reaction.message.guild.roles, id=897183478871916604) # Muhalif rolu
        if discord.utils.get(user.roles, id=897183478871916604) != None:
            await reaction.message.channel.send('Zaten alakali rolunuz mevcut.')
        elif discord.utils.get(user.roles, id=895339339293261875) != None:
            await reaction.message.channel.send('Zaten Erdoganci rolunuz mevcut.')
        else:
            await user.add_roles(muhalif)
            await reaction.message.channel.send('Rolunuz verildi.')
    if reaction.emoji == "2️⃣":
        erdoganci = discord.utils.get(reaction.message.guild.roles, id=895339339293261875) # Erdoganci rolu
        if discord.utils.get(user.roles, id=895339339293261875) != None:
            await reaction.message.channel.send('Zaten alakali rolunuz mevcut.')
        elif discord.utils.get(user.roles, id=897183478871916604) != None:
            await reaction.message.channel.send('Zaten Muhalif rolunuz mevcut.')
        else:
            await user.add_roles(erdoganci)
            await reaction.message.channel.send('Rolunuz verildi.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Komut bulunamadi.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("Bu komutu kullanmak icin yeterli yetkin yok.")
    else:
        raise error


for cog in cogs:
    client.load_extension(cog)
client.run(token)
