#explicit content removal and banning the user
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def is_explicit(url):
    explicit_keywords = ["explicit", "nsfw", "adult", "onlyfans"]
    return any(keyword in url for keyword in explicit_keywords)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {member.guild.name}!'
    )
    
async def on_message(message):
    if message.author == bot.user:
        return

    for word in message.content.split():
        if word.startswith("http://") or word.startswith("https://"):
            if is_explicit(word):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, you have been banned for posting explicit content.")
                await message.author.ban(reason="Posted explicit content")
                return
            
    if "lol" in message.content.lower():
        print("Detected 'lol' in message")
        await message.channel.send("u so skibidi")
        
    await bot.process_commands(message)

bot.run("MTI2MjM3NjQ1Nzc5NjA1OTE5OQ.GSjwlU.vtTwtqWUmcVfPWuvlAbAsZocN52PMaNtxdMz68")
