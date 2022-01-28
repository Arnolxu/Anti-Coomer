import discord
from discord.ext import commands
import bot
from bot import client
import random as rndm
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @client.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(description=f"{member.display_name} adli kisi yasaklandi.", color=0xed1822)
        await ctx.send(embed=embed)

    @client.command()
    @commands.has_permissions(administrator=True)
    async def unban(ctx, id: int):
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(description=f"{user.display_name} adli kisinin yasagi kaldirildi.", color=0xed1822)
        await ctx.send(embed=embed)

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
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        embed = discord.Embed(description=f"{user.display_name} adli kisi atildi.", color=0xed1822)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Moderation(bot))