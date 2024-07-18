import discord
from discord.ext import commands
from transformers import pipeline
import warnings

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def summarize_text(text):
    summary = summarizer(text, max_length=100, min_length=20, do_sample=False)
    return summary[0]['summary_text']

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    sentiment = result[0]['label']
    return sentiment

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True 
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def is_explicit(url):
    explicit_keywords = ["explicit", "nsfw", "adult", "onlyfans"]
    return any(keyword in url.lower() for keyword in explicit_keywords)

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
                await message.channel.send(f"{message.author.mention}, you have been fanum taxed for posting explicit content.") # fanum taxxed = banned
                return
            
    if message.content.lower().startswith("!summarize"):
        text_to_summarize = message.content[len("!summarize "):]
        if len(text_to_summarize) > 50:  #minimum length for summarization
            summary = summarize_text(text_to_summarize)
            await message.channel.send(f"Summary: {summary}")
        else:
            await message.channel.send("Please provide a longer text to summarize.")

    if len(message.content) > 50:
        sentiment = analyze_sentiment(message.content)
        if sentiment == "NEGATIVE":
            await message.channel.send("Bro wut u doin? 😔")
        elif sentiment == "POSITIVE":
            await message.channel.send("Damn u cooked 😄")

    if "sadge" in message.content.lower() or "sad" in message.content.lower() or "sed" in message.content.lower():
        await message.channel.send("big L") # big L = big loss
    if "damn" in message.content.lower() or "demn" in message.content.lower() or "dang" in message.content.lower() or "deng" in message.content.lower():
        await message.channel.send("big W") # big W = big win
    if "lol" in message.content.lower() or "lmao" in message.content.lower() or "lmfao" in message.content.lower() or "xD" in message.content.lower():
        await message.channel.send("so skibidi") # so skibidi = so true
    if "bruh" in message.content.lower() or "bro" in message.content.lower() or "bruh" in message.content.lower() or "ain't no way" in message.content.lower():
        await message.channel.send("bro's gotta cook")
    if "legit" in message.content.lower():
        await message.channel.send("smh") # smh = shaking my head
    if "lit" in message.content.lower() or "fire" in message.content.lower() or "sick" in message.content.lower() or "dope" in message.content.lower() or "sheesh" in message.content.lower():
        await message.channel.send("🔥") 
    if "savage" in message.content.lower() or "savage af" in message.content.lower():
        await message.channel.send("ikr") # ikr = i know right
    if "flex" in message.content.lower() or "flexing" in message.content.lower():
        await message.channel.send("💪") 
    if "sigh" in message.content.lower() or "sighh" in message.content.lower() or "sighhh" in message.content.lower():
        await message.channel.send("😔")
    if "f" in message.content.lower() or "tf" in message.content.lower() or "wtf" in message.content.lower():
        await message.channel.send("lmao")
    if "huh" in message.content.lower() or "wut" in message.content.lower() or "what" in message.content.lower():
        await message.channel.send(f"{message.author.mention}, duh")
    if "ngl" in message.content.lower() or "let him cook" in message.content.lower():
        await message.channel.send("fr") # fr = for real
    if "ikr" in message.content.lower():
        await message.channel.send("us")
    if "same" in message.content.lower() or "sem" in message.content.lower():
        await message.channel.send("no cap") # no cap = no lie
    if "no cap" in message.content.lower():
        await message.channel.send("fax")
    if "cringe" in message.content.lower():
        await message.channel.send("fax fr") # fax fr = facts for real
    if "why are u gay" in message.content.lower() or "why u gay" in message.content.lower() or "gay" in message.content.lower():
        await message.channel.send("no u")
    if "legit" in message.content.lower() or "no cap" in message.content.lower():
        await message.channel.send("bet") # bet = agreed
        
    await bot.process_commands(message)
bot.run("token")
