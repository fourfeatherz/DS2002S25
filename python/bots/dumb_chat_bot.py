import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

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

    if "how are you" in content:
        await message.channel.send("I'm feeling electric today! ⚡ How about you?")
    elif "bye" in content:
        await message.channel.send("Goodbye! Don't forget to unplug your toaster. 🥪")
    elif "joke" in content:
        await message.channel.send("Why don't skeletons fight each other? They don't have the guts. 😂")

    await bot.process_commands(message)
    
bot.run('your_token')



