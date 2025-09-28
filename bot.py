import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import datetime
import asyncio

load_dotenv()
TOKEN = os.getenv("swtoken")

ROLE_NAME = "Citizen of Etheria"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

if os.path.exists("feeding_data.json"):
    with open("feeding_data.json", "r") as f:
        feeding_data = json.load(f)
else:
    feeding_data = {}

ACHIEVEMENTS = {
    5: {"text": "🍎 Caring Friend – Fed Swift Wind 5 times!", "role": "Caring Friend"},
    10: {"text": "🌟 Loyal Companion – Fed Swift Wind 10 times!", "role": "Loyal Companion"},
    20: {"text": "🏅 Hero of Etheria – Fed Swift Wind 20 times!", "role": "Hero of Etheria"},
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    if member.bot:
        print(f"🤖 Skipping role assignment for bot: {member.name}")
        return

    role = discord.utils.get(member.guild.roles, name=ROLE_NAME)
    if role:
        await member.add_roles(role)
        print(f"🌟 Assigned {ROLE_NAME} to {member.name}")
    else:
        print(f"⚠️ Role '{ROLE_NAME}' not found in {member.guild.name}")

@bot.command()
async def feed(ctx, member: discord.Member = None):

    if not member or not member.bot:
        await ctx.send("You must tag **@Swift Wind** to feed them!")
        return

    user_id = str(ctx.author.id)
    today = str(datetime.date.today())

    if user_id not in feeding_data:
        feeding_data[user_id] = {"last_feed": None, "count": 0}

    user_data = feeding_data[user_id]

    if user_data["last_feed"] == today:
        await ctx.send(f"⏳ {ctx.author.mention}, you already fed me today! try again tomorrow")
        return

    user_data["count"] += 1
    user_data["last_feed"] = today
    feeding_data[user_id] = user_data

    with open("feeding_data.json", "w") as f:
        json.dump(feeding_data, f, indent=2)

    embed = discord.Embed(
        title="🥕 Swift Wind has been fed!",
        description=f"{ctx.author.mention} fed Swift Wind today!\nTotal feeds: **{user_data['count']}**",
        color=discord.Color.green()
    )

    file_path = "images/swiftwind-unicorn.gif"
    if os.path.exists(file_path):
        file = discord.File(file_path, filename="swiftwind-unicorn.gif")
        embed.set_thumbnail(url="attachment://swiftwind-unicorn.gif")
        await ctx.send(file=file, embed=embed)
    else:
        await ctx.send(embed=embed)

    if user_data["count"] in ACHIEVEMENTS:
        achievement = ACHIEVEMENTS[user_data["count"]]
        achievement_text = achievement["text"]
        embed.add_field(name="🏆 Achievement Unlocked!", value=achievement_text, inline=False)

        role_name = achievement["role"]
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if not role:
            role = await ctx.guild.create_role(
                name=role_name,
                reason=f"Role Not Found! and Was Auto-created by Me: {role_name}"
            )

        await ctx.author.add_roles(role)
        embed.add_field(name="🎖 Role Awarded", value=f"You’ve been given the **{role_name}** role!", inline=False)

        await ctx.send(embed=embed)

@bot.command()
async def brush(ctx, member: discord.Member = None):

    if not member or not member.bot:
        await ctx.send("You must tag **@Swift Wind** to brush their mane!")
        return

    user_id = str(ctx.author.id)
    today = str(datetime.date.today())

    if "brush" not in feeding_data.get(user_id, {}):
        feeding_data[user_id] = feeding_data.get(user_id, {})
        feeding_data[user_id]["brush"] = {"last": None, "count": 0}

    brush_data = feeding_data[user_id]["brush"]

    if brush_data["last"] == today:
        await ctx.send(f"⏳ {ctx.author.mention}, you already brushed Me today! Try again tomorrow.")
        return
      
    brush_data["count"] += 1
    brush_data["last"] = today
    feeding_data[user_id]["brush"] = brush_data

    with open("feeding_data.json", "w") as f:
        json.dump(feeding_data, f, indent=2)

    embed = discord.Embed(
        title="🪮 Swift Wind’s mane shines brighter!",
        description=f"{ctx.author.mention} brushed Swift Wind today!\nTotal brushes: **{brush_data['count']}**",
        color=discord.Color.blue()
    )

    file_path = "images/swiftwind-brush.gif"
    if os.path.exists(file_path):
        file = discord.File(file_path, filename="swiftwind-brush.gif")
        embed.set_thumbnail(url="attachment://swiftwind-brush.gif")
        await ctx.send(file=file, embed=embed)
    else:
        await ctx.send(embed=embed)


bot.run(TOKEN)
