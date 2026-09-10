import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is None:
            return

        embed = discord.Embed(
            title=f"Welcome to {member.guild.name}!",
            description=f"Hello {member.mention}! We're glad to have you here.\n"
            f"Check out #rules and enjoy your stay!",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Member #{member.guild.member_count}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel is None:
            return

        embed = discord.Embed(
            title="Member Left",
            description=f"**{member}** has left the server.",
            color=discord.Color.red(),
        )
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
