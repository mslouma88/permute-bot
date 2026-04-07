import os
import discord
from discord.ext import commands
from parser_pdf import parse_planning
from database import init_db, add_shift, get_shift, get_agents, add_agent
from scheduler import find_replacements

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

init_db()

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Bot opérationnel")

# -------------------------
# Ajouter agent
# -------------------------

@bot.command()
async def addagent(ctx, name, discord_id):

    add_agent(name, discord_id)

    await ctx.send(f"Agent {name} ajouté")

# -------------------------
# Upload planning
# -------------------------

@bot.command()
async def uploadplanning(ctx):

    if not ctx.message.attachments:
        await ctx.send("Envoyer un PDF")
        return

    file = ctx.message.attachments[0]

    path = f"./{file.filename}"

    await file.save(path)

    planning = parse_planning(path)

    for p in planning:

        add_shift(
            p["date"],
            p["agent"],
            p["shift"]
        )

    await ctx.send("Planning importé")

# -------------------------
# Demande permute
# -------------------------

@bot.command()
async def permute(ctx, date):

    requester = str(ctx.author.id)

    shift = get_shift(requester, date)

    if not shift:
        await ctx.send("Aucune vacation ce jour")
        return

    replacements = find_replacements(date, shift)

    if not replacements:
        await ctx.send("Aucun remplaçant disponible")
        return

    for r in replacements:

        user = await bot.fetch_user(int(r))

        await user.send(
            f"Remplacement possible le {date}. Répondre !accept"
        )

    await ctx.send("Demande envoyée")

# -------------------------
# Acceptation
# -------------------------

@bot.command()
async def accept(ctx):

    await ctx.send("Permute acceptée. En attente validation chef.")

bot.run(TOKEN)