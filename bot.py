import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "cogs.moderation",
    "cogs.music",
    "cogs.welcome",
    "cogs.logging",
]


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="!help for commands"))


@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! {latency}ms")


@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
    embed.add_field(name="!ping", value="Check bot latency", inline=False)
    embed.add_field(name="!kick @user [reason]", value="Kick a member", inline=False)
    embed.add_field(name="!ban @user [reason]", value="Ban a member", inline=False)
    embed.add_field(name="!unban user#discriminator", value="Unban a member", inline=False)
    embed.add_field(name="!mute @user [reason]", value="Timeout a member", inline=False)
    embed.add_field(name="!unmute @user", value="Remove timeout from a member", inline=False)
    embed.add_field(name="!play <query>", value="Play a song", inline=False)
    embed.add_field(name="!stop", value="Stop music and clear queue", inline=False)
    embed.add_field(name="!skip", value="Skip current song", inline=False)
    embed.add_field(name="!queue", value="Show music queue", inline=False)
    await ctx.send(embed=embed)


async def setup():
    for cog in COGS:
        await bot.load_extension(cog)
        print(f"Loaded {cog}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(setup())
    bot.run(TOKEN)
