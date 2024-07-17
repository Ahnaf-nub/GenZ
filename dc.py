import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True 
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

def is_explicit(url):
    explicit_keywords = ["explicit", "nsfw", "adult", "onlyfans"]
    return any(keyword in url.lower() for keyword in explicit_keywords)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")

    if message.author == bot.user:
        print("Message from bot itself, ignoring.")
        return

    # Check for explicit links
    for word in message.content.split():
        if word.startswith("http://") or word.startswith("https://") or word.startswith("www."):
            if is_explicit(word):
                print(f"Explicit link found: {word}")
                await message.delete()
                await message.channel.send(f"{message.author.mention}, you have been banned for posting explicit content.")
                await message.author.ban(reason="Posted explicit content")
                return

    if "sadge" in message.content.lower() or "sad" in message.content.lower() or "sed" in message.content.lower():
        await message.channel.send("big L")
    if "damn" in message.content.lower() or "demn" in message.content.lower() or "dang" in message.content.lower() or "deng" in message.content.lower():
        await message.channel.send("big W")
    if "lol" in message.content.lower() or "lmao" in message.content.lower() or "lmfao" in message.content.lower():
        await message.channel.send("so skibidi")
    
    await bot.process_commands(message)

bot.run("token")
