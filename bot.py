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

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(description=f"{user.display_name} adli kisi yasaklandi.", color=0xed1822)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, id: int):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    embed = discord.Embed(description=f"{user.display_name} adli kisinin yasagi kaldirildi.", color=0xed1822)
    await ctx.send(embed=embed)

@client.command(help="Yazi tura atar, sonuc rastgeledir.")
async def yazitura(ctx):
    result = rndm.choice(["Yazi", "Tura"])
    await ctx.send(result)

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

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
    await user.kick(reason=reason)
    embed = discord.Embed(description=f"{user.display_name} adli kisi atildi.", color=0xed1822)
    await ctx.send(embed=embed)

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

@client.command(help="Uye hakkinda bilgi verir")
async def minfo(ctx, member: typing.Optional[discord.Member]):
    if member == None:
        member = ctx.author
    if member.bot:
        kullanici_botmu = "Evet"
    else:
        kullanici_botmu = "Hayir"

    kullanici_id = member.id
    kullanici_rolleri_list = [r.mention for r in member.roles if r != ctx.guild.default_role]
    kullanici_butun_roller_fix = ", ".join(kullanici_rolleri_list)
    kullanici_sunucuya_giris_obj = str(member.joined_at)
    kullanici_bolunmus_sunucuya_giris = kullanici_sunucuya_giris_obj.split(".")
    kullanici_sunucuya_giris = kullanici_bolunmus_sunucuya_giris[0]
    kullanici_hesap_tarihi_obj = str(member.created_at)
    kullanici_bolunmus_hesap_tarihi = kullanici_hesap_tarihi_obj.split(".")
    kullanici_hesap_tarihi = kullanici_bolunmus_hesap_tarihi[0]

    embed = discord.Embed(title=f"{member.name} Adli Kişinin Detaylari", description=f"**Kullanici ID:**\n{kullanici_id}\n\n**Bot mu?**\n{kullanici_botmu}\n\n**Roller ({len(kullanici_rolleri_list)}):**\n{kullanici_butun_roller_fix}\n\n**Sunucuya Giriş Tarihi:**\n{kullanici_sunucuya_giris}\n\n**Hesap Oluşturma Tarihi:**\n{kullanici_hesap_tarihi}", color=0xed1822)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

@commands.guild_only()
@client.command(help="Bot hakkinda bilgi verir.")
async def stats(ctx):
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1
    embed = discord.Embed(description=f"""
Sunucu sayisi: **{str(servers)}**
Üye sayisi: **{str(members)}**
API Pingi: **{str(int(client.latency * 1000))}**
Donus Pingi: olcüyorum..
İşlemci: **{funcs.get_processor_name()}**
RAM: **{funcs.get_ram()}**
""", color=0XFF1123)
    before = time.monotonic()
    msg = await ctx.send(embed=embed)
    ping = (time.monotonic() - before) * 1000
    embed = discord.Embed(description=f"""
Sunucu sayisi: **{str(servers)}**
Üye sayisi: **{str(members)}**
API Pingi: **{str(int(client.latency * 1000))}**
Donus Pingi: **{int(ping)}**
İşlemci: **{funcs.get_processor_name()}**
RAM: **{funcs.get_ram()}**
""", color=0XFF1123)
    await msg.edit(embed=embed)

@client.command(help="Verdiginiz listeden rastgele bir sey secer.")
async def random(ctx, *things):
    if things == ('never', 'gonna', 'give', 'you', 'up'):
        await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    else:
        await ctx.send(rndm.choice(things))

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

@client.command()
async def avatar(ctx, member=None):
    if(member != None):
        if(member[0] == "<"):
            mbr =member.replace("<","").replace(">","").replace("@","").replace("!","")
            av = await client.fetch_user(mbr)
            embed = discord.Embed(title="Avatar URL",url=f"{av.avatar_url}")
            embed.set_image(url=f"{av.avatar_url}")
            await ctx.send(embed=embed)

        
    if member == None:
        member = ctx.author
        show_avatar = discord.Embed(
            title="Avatar URL",
            url=f"{member.avatar_url}",
            color = discord.Color.green()
        )
        show_avatar.set_image(url="{}".format(member.avatar_url))
        await ctx.send(embed=show_avatar)

    if type(member) == str:
        c = len(str(member))
        for i in ctx.guild.members:
            a = str(i).lower()
            if a[0:c] == str(member).lower():
                show_avatar = discord.Embed(
                    title="Avatar URL",
                    url=f"{i.avatar_url}",
                    color = discord.Color.green()
                )
                show_avatar.set_image(url="{}".format(i.avatar_url))
                await ctx.send(embed=show_avatar)
                break

@client.command()
async def sinfo(ctx):

        server = ctx.message.guild

        roles = str(len(server.roles))
        emojis = str(len(server.emojis))
        channels = str(len(server.channels))
        owner = await client.fetch_user(server.owner_id)

        embed = discord.Embed(title=server.name, description='Sunucu Bilgisi', color=0XFF1123)
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Olusturulma tarihi:", value=server.created_at.strftime('%d %B %Y at %H:%M UTC+3'), inline=False)
        embed.add_field(name="Sunucu ID'si:", value=server.id, inline=False)
        embed.add_field(name="Uye sayisi:", value=server.member_count, inline=True)
        embed.add_field(name="Sunucu Sahibi:", value=owner.name, inline=True)
        embed.add_field(name="Sunucu Bolgesi:", value=string.capwords(str(server.region)), inline=True)
        embed.add_field(name="Onaylama Seviyesi:", value=str(server.verification_level).replace("none", "Yok").replace("low", "Dusuk").replace("medium", "Orta").replace("high", "Yuksek").replace("extreme", ""), inline=True)
        embed.add_field(name="Rol Sayisi:", value=roles, inline=True)
        embed.add_field(name="Emoji Sayisi:", value=emojis, inline=True)
        embed.add_field(name="Kanal Sayisi:", value=channels, inline=True)

        await ctx.send(embed=embed) \


@client.event
async def on_member_join(member):
    text = """Esenlikler,  Ittihat ve Terakki'ye hoşgeldin,\n{}.""".format(member.display_name)
    member.id = 
    text_2 = '''Burda sosyal medyada 
yaymak icin propaganda 
üretip yayınlıyoruz. 
#chp-propaganda'ya 
atabilirsin'''
    img = Image.open('sickbackground.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 27)
    draw.text((165,28), text, (0, 0, 0), font=font, stroke_width=2, stroke_fill=(255, 255, 255))
    draw.text((165,100), text_2, (0, 0, 0), font=font, stroke_width=2, stroke_fill=(255, 255, 255))
    img.save("text.png")
    channel = client.get_channel(894685294010445854)
    await channel.send(f'Esenlikler! <@{member.id}> ')
    await channel.send(file=discord.File("text.png"))

client.run(token)
