import discord
from discord.ext import commands
from transformers import pipeline
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('token')
API_KEY = os.getenv('gemini')

app = Flask(__name__)

GOOGLE_API_KEY = API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True 
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)
@app.route('/')
def home():
    return 'Discord Bot with Flask Server Running'
def run_flask():
    app.run(host='0.0.0.0', port=5000)

def summarize_text(text):
    summary = model.generate_content(f"Summarize {text} within a maximum length of 100 and a minimum length of 20.")
    return summary

def analyze_sentiment(text):
    sentiment = model.generate_content(f"What is the sentiment of {text} within (joy, sadness, anger, fear, disgust, surprise, neutral)?")
    return sentiment

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
                await message.channel.send(f"Summary: {summary.text}")
            elif message.content.lower() == "!summarize":
                await message.channel.send("GenZ bot can now provide text summaries upon request using an NLP model. Send a message starting with !summarize followed by a long text.")
            else:
                await message.channel.send("Please provide a longer text to summarize.")

        if len(message.content) > 40:
            sentiment = analyze_sentiment(message.content).text
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
        if "lit" in message.content.lower() or "fire" in message.content.lower() or "dope" in message.content.lower() or "sheesh" in message.content.lower():
            await message.channel.send("🔥")
        if "savage" in message.content.lower() or "savage af" in message.content.lower():
            await message.channel.send("ikr") # ikr = i know right
        if "flex" in message.content.lower() or "flexing" in message.content.lower():
            await message.channel.send("💪")
        if "sigh" in message.content.lower() or "sighh" in message.content.lower() or "sighhh" in message.content.lower():
            await message.channel.send("😔")
        if "tf" in message.content.lower() or "wtf" in message.content.lower():
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

def run_discord_bot():
    bot.run(TOKEN)
if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    run_discord_bot()
