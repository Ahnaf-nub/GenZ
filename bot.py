import discord
from discord.ext import commands
import requests

# Define API URLs and headers
sentiment_API = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
summarizer_API = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer api_key"}  # Replace 'api_key' with your actual HuggingFace API key

# Functions to query APIs
def query_summarize(payload):
    try:
        response = requests.post(summarizer_API, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during summarization: {e}")
        return None

def query_sentiment(payload):
    try:
        response = requests.post(sentiment_API, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during sentiment analysis: {e}")
        return None

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True 
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# Function to summarize text
def summarize_text(text):
    summary_response = query_summarize({"inputs": text})
    if summary_response:
        return summary_response[0].get('summary_text', "No summary available.")
    else:
        return "Error occurred while summarizing."

# Function to analyze sentiment
def analyze_sentiment(text: str):
    sentiment_response = query_sentiment({"inputs": text})
    if sentiment_response:
        try:
            return sentiment_response[0][0]['label']
        except (KeyError, IndexError, TypeError):
            return "unknown"
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

# Message handling
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
                await message.channel.send("Everything's gonna be alright real soon")
            elif sentiment == "disgust":
                await message.channel.send("tf fr")
            elif sentiment == "surprise":
                await message.channel.send("Sheesh, that's dope!")
            elif sentiment == "neutral":
                await message.channel.send("I see.")

        # Check for slang words and phrases
        lower_content = message.content.lower()
        response_map = {
            "sadge": "big L",
            "sad": "big L",
            "sed": "big L",
            "damn": "big W",
            "demn": "big W",
            "dang": "big W",
            "deng": "big W",
            "lol": "so skibidi",
            "lmao": "so skibidi",
            "lmfao": "so skibidi",
            "xd": "so skibidi",
            "bruh": "bro's gotta cook",
            "bro": "bro's gotta cook",
            "ain't no way": "bro's gotta cook",
            "legit": "smh",
            "lit": "🔥",
            "fire": "🔥",
            "dope": "🔥",
            "sheesh": "🔥",
            "savage": "ikr",
            "savage af": "ikr",
            "flex": "💪",
            "flexing": "💪",
            "sigh": "😔",
            "sighh": "😔",
            "sighhh": "😔",
            "wtf": "lmao",
            "huh": f"{message.author.mention}, duh",
            "wut": f"{message.author.mention}, duh",
            "what": f"{message.author.mention}, duh",
            "ngl": "fr",
            "let him cook": "fr",
            "ikr": "fr",
            "no cap": "fax",
            "cringe": "fax fr",
            "why are u gay": "no u",
            "why u gay": "no u",
            "gay": "no u",
        }

        for key, response in response_map.items():
            if key in lower_content:
                await message.channel.send(response)
                break

    await bot.process_commands(message)

# Make sure to replace the token with your actual bot token securely
bot.run("your_token_here")
