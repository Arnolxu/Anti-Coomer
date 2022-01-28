import discord
from discord.ext import commands
from bot import client
from bot import *
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
        await ctx.send(embed=embed) 
    @client.command(help="Yazi tura atar, sonuc rastgeledir.")
    async def yazitura(ctx):
        result = rndm.choice(["Yazi", "Tura"])
        await ctx.send(result)
    @client.command(help="Verdiginiz listeden rastgele bir sey secer.")
    async def random(ctx, *things):
        if things == ('never', 'gonna', 'give', 'you', 'up'):
            await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        else:
            await ctx.send(rndm.choice(things))
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

def setup(bot):
    bot.add_cog(Utils(bot))