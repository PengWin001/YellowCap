import discord
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        channel = message.guild.system_channel
        if channel is None:
            return

        embed = discord.Embed(
            title="Message Deleted",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Author", value=message.author.mention, inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Content", value=message.content[:1024] or "*(empty)*", inline=False)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.content == after.content:
            return

        channel = before.guild.system_channel
        if channel is None:
            return

        embed = discord.Embed(
            title="Message Edited",
            color=discord.Color.yellow(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Author", value=before.author.mention, inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        embed.add_field(name="Before", value=before.content[:1024] or "*(empty)*", inline=False)
        embed.add_field(name="After", value=after.content[:1024] or "*(empty)*", inline=False)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        channel = messages[0].guild.system_channel
        if channel is None:
            return
        embed = discord.Embed(
            title="Bulk Delete",
            description=f"**{len(messages)}** messages were deleted in {messages[0].channel.mention}",
            color=discord.Color.red(),
        )
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logging(bot))
