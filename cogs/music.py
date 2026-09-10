import asyncio
import discord
from discord.ext import commands
from collections import deque

queues = {}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_queue(self, guild_id):
        if guild_id not in queues:
            queues[guild_id] = deque()
        return queues[guild_id]

    @commands.command(name="play")
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            return await ctx.send("Join a voice channel first.")

        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await channel.connect()
        else:
            vc = ctx.voice_client

        # Note: For full music functionality, integrate with wavelink or yt-dlp.
        # This is a simplified version that demonstrates the structure.
        embed = discord.Embed(title="Added to Queue", description=f"**{query}**", color=discord.Color.purple())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

        queue = self.get_queue(ctx.guild.id)
        queue.append(query)

        if not vc.is_playing():
            await self._play_next(ctx, vc)

    async def _play_next(self, ctx, vc):
        queue = self.get_queue(ctx.guild.id)
        if not queue:
            if vc.is_connected():
                await vc.disconnect()
            return

        song = queue.popleft()
        embed = discord.Embed(title="Now Playing", description=f"**{song}**", color=discord.Color.green())
        await ctx.send(embed=embed)

        # In production, use wavelink or a similar library to actually play audio.
        # For now, wait 30 seconds then try the next song.
        await asyncio.sleep(30)
        await self._play_next(ctx, vc)

    @commands.command(name="stop")
    async def stop(self, ctx):
        if ctx.voice_client:
            queues[ctx.guild.id] = deque()
            ctx.voice_client.stop()
            await ctx.send("Music stopped and queue cleared.")

    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped!")
        else:
            await ctx.send("Nothing is playing.")

    @commands.command(name="queue")
    async def queue_display(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        if not queue:
            return await ctx.send("The queue is empty.")

        embed = discord.Embed(title="Music Queue", color=discord.Color.blue())
        for i, song in enumerate(list(queue)[:10], 1):
            embed.add_field(name=f"{i}.", value=song, inline=False)
        if len(queue) > 10:
            embed.set_footer(text=f"And {len(queue) - 10} more...")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))
