import discord
from discord.ext import commands
import requests

# --- SETTINGS ---
GROQ_API_KEY = "your-groq-api-key"  # <<<<< Replace with your real Groq API key
DISCORD_BOT_TOKEN = "your-discord-bot-token"  # <<<<< Replace with your real Discord Bot token

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# --- GROQ API FUNCTION ---

async def ask_groq(user_message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Groq API error: {e}")
        return "Sorry, I'm having a brain freeze. 🧊 Try again later!"

# --- UTILITY: Send Long Messages Safely ---

async def send_long_message(channel, content):
    # Send message in chunks of max 2000 characters
    for i in range(0, len(content), 2000):
        await channel.send(content[i:i+2000])

# --- EVENTS & COMMANDS ---

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}! 👋")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Uh-oh, I don't know that command! Try `!hello`.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    # Basic keyword responses
    if "how are you" in content:
        await message.channel.send("I'm feeling electric today! ⚡ How about you?")
    elif "bye" in content:
        await message.channel.send("Goodbye! Don't forget to unplug your toaster. 🥪")
    elif "joke" in content:
        await message.channel.send("Why don't skeletons fight each other? They don't have the guts. 😂")
    elif message.content.startswith('!'):
        await bot.process_commands(message)
    else:
        # Everything else: use Groq AI
        reply = await ask_groq(message.content)
        await send_long_message(message.channel, reply)

    await bot.process_commands(message)

# --- START BOT ---

bot.run(DISCORD_BOT_TOKEN)
