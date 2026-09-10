import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You cannot kick someone with an equal or higher role.")
        await member.kick(reason=reason)
        embed = discord.Embed(title="Member Kicked", color=discord.Color.orange())
        embed.add_field(name="User", value=member.mention)
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You cannot ban someone with an equal or higher role.")
        await member.ban(reason=reason)
        embed = discord.Embed(title="Member Banned", color=discord.Color.red())
        embed.add_field(name="User", value=member.mention)
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_name):
        banned_users = [entry async for entry in ctx.guild.bans()]
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name.lower() == member_name.lower() or str(user) == member_name:
                await ctx.guild.unban(user)
                embed = discord.Embed(title="Member Unbanned", color=discord.Color.green())
                embed.add_field(name="User", value=str(user))
                await ctx.send(embed=embed)
                return
        await ctx.send(f"User `{member_name}` not found in ban list.")

    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int = 10, *, reason="No reason provided"):
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You cannot mute someone with an equal or higher role.")
        duration = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        embed = discord.Embed(title="Member Muted", color=discord.Color.yellow())
        embed.add_field(name="User", value=member.mention)
        embed.add_field(name="Duration", value=f"{minutes} minutes")
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name="unmute")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        embed = discord.Embed(title="Member Unmuted", color=discord.Color.green())
        embed.add_field(name="User", value=member.mention)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
