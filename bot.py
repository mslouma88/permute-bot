import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot connecté")

@bot.command()
async def permute(ctx, date):
    await ctx.send(f"Demande de permute pour {date}")

@bot.command()
async def accept(ctx):
    await ctx.send("Permute acceptée")

bot.run(TOKEN)