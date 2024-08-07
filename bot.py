import discord
from discord.ext import commands
import requests

# Define API URLs and headers
sentiment_API = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
summarizer_API = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer api_key"}

# Functions to query APIs
def query_summarize(payload):
    response = requests.post(summarizer_API, headers=headers, json=payload)
    return response.json()

def query_sentiment(payload):
    response = requests.post(sentiment_API, headers=headers, json=payload)
    return response.json()

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True 
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# Function to summarize text
def summarize_text(text):
    summary = query_summarize({"inputs": text})
    return summary[0]['summary_text']

# Function to analyze sentiment
def analyze_sentiment(text: str):
    sentiment = query_sentiment({"inputs": text})
    try:
        # Access the first dictionary in the first list and get the label
        return sentiment[0][0]['label']
    except (KeyError, IndexError, TypeError) as e:
        return "unknown"

# Function to check for explicit links
def is_explicit(url):
    explicit_keywords = ["explicit", "nsfw", "adult", "onlyfans"]
    return any(keyword in url.lower() for keyword in explicit_keywords)

# Summarize command
@bot.command()
async def summarize(ctx, *, text: str):
    if len(text) > 50:
        summary = summarize_text(text)
        await ctx.send(f"Summary: {summary}")
    else:
        await ctx.send("Please provide a longer text to summarize.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for explicit links
    for word in message.content.split():
        if word.startswith(("http://", "https://", "www.")) and is_explicit(word):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you have been fanum taxed for posting explicit content.")
            return

    # Skip sentiment analysis if the message is a command
    if not message.content.startswith("!"):
        if len(message.content) > 50:
            sentiment = analyze_sentiment(message.content)
            if sentiment == "joy":
                await message.channel.send("Demn!")
            elif sentiment == "sadness":
                await message.channel.send("Sadge, sorry to hear that")
            elif sentiment == "anger":
                await message.channel.send("Bruh kalm down")
            elif sentiment == "fear":
                await message.channel.send("everythings gonna be ight real soon")
            elif sentiment == "disgust":
                await message.channel.send("tf fr")
            elif sentiment == "surprise":
                await message.channel.send("sheesh that's dope")
            elif sentiment == "neutral":
                await message.channel.send("i see")

    if not message.content.startswith("!"):
        if "sadge" in message.content.lower() or "sad" in message.content.lower() or "sed" in message.content.lower():
            await message.channel.send("big L")
        if "damn" in message.content.lower() or "demn" in message.content.lower() or "dang" in message.content.lower() or "deng" in message.content.lower():
            await message.channel.send("big W")
        if "lol" in message.content.lower() or "lmao" in message.content.lower() or "lmfao" in message.content.lower() or "xd" in message.content.lower():
            await message.channel.send("so skibidi")
        if "bruh" in message.content.lower() or "bro" in message.content.lower() or "ain't no way" in message.content.lower():
            await message.channel.send("bro's gotta cook")
        if "legit" in message.content.lower():
            await message.channel.send("smh")
        if "lit" in message.content.lower() or "fire" in message.content.lower() or "dope" in message.content.lower() or "sheesh" in message.content.lower():
            await message.channel.send("🔥")
        if "savage" in message.content.lower() or "savage af" in message.content.lower():
            await message.channel.send("ikr")
        if "flex" in message.content.lower() or "flexing" in message.content.lower():
            await message.channel.send("💪")
        if "sigh" in message.content.lower() or "sighh" in message.content.lower() or "sighhh" in message.content.lower():
            await message.channel.send("😔")
        if "wtf" in message.content.lower():
            await message.channel.send("lmao")
        if "huh" in message.content.lower() or "wut" in message.content.lower() or "what" in message.content.lower():
            await message.channel.send(f"{message.author.mention}, duh")
        if "ngl" in message.content.lower() or "let him cook" in message.content.lower():
            await message.channel.send("fr")
        if "ikr" in message.content.lower():
            await message.channel.send("fr")
        if "no cap" in message.content.lower():
            await message.channel.send("fax")
        if "cringe" in message.content.lower():
            await message.channel.send("fax fr")
        if "why are u gay" in message.content.lower() or "why u gay" in message.content.lower() or "gay" in message.content.lower():
            await message.channel.send("no u")
        if "legit" in message.content.lower() or "no cap" in message.content.lower():
            await message.channel.send("bet")

    await bot.process_commands(message)
bot.run("")
