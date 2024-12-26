import gambling
import discord
from discord.ext import commands
import random
import asyncio
from googlesearch import search
import os

# Variables and Lists
memes = ["https://i.pinimg.com/1200x/83/f0/5d/83f05d92bd0c1a3babbbc330e9310622.jpg", "https://pbs.twimg.com/media/F1HNuiSWwAItcxE?format=jpg&name=large", "https://staging.cohostcdn.org/attachment/677ce999-9a8a-4412-83d4-be92e7d543d7/image.png?width=675&auto=webp&dpr=1", "https://i.redd.it/his-ass-is-playing-the-piano-v0-ob55pt6zd9ad1.jpg?width=1088&format=pjpg&auto=webp&s=aa4c38e3f4e86dddefdd8562a01c8de80d1f86f7", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtRVE2Jp6R5kH9svSpg4nNjAR5fZ9qA-hduA&s"]
feedback_file = "Feedback.txt"

# Functions
def create_deck():
    deck = [(str(i), i) for i in range(1, 11)] * 4
    deck += [("Jack", 10), ("Queen", 10), ("King", 10)] * 4
    random.shuffle(deck)
    return deck

def draw_card():
    deck = create_deck()
    suit = ["Spades", "Clubs", "Hearts", "Diamonds"]
    card = deck.pop()
    return random.choice(suit), card

# Bot Setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print([command.name for command in bot.commands])

'''
async def load():
    for filename in os.listdir('./cogs/leveling_system'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.leveling_system.{filename[:-3]}')
                print(f'Loaded {filename}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e}')
'''

#--------------------------------------------------------------------------------------------COMMANDS----------------------------------------------------------=====--------------------------------------------------------#

#Commands from gambling.py
bot.add_command(gambling.flipcoin)
bot.add_command(gambling.rolldice)
bot.add_command(gambling.drawcard)
bot.add_command(gambling.blackjack)

# Command to greet the bot
@bot.command()
async def hello(ctx):
    await ctx.send("i am freddy fazbore")

# blame jimmy for this
@bot.command()
async def merrychristmas(ctx):
    embed = discord.Embed (title="merry christmas", description="hohoho")
    embed.set_image(url="https://media.tenor.com/RFqq13DGbKYAAAAM/jolly-christmas-posting.gif")
    await ctx.send(embed=embed)

# Command to have a random meme from a list
@bot.command()
async def randomletter(ctx):
    choice = random.choice(memes)
    await ctx.send("Random letter: " + choice)

# Command to search google
@bot.command()
async def google(ctx, *, query):
    await ctx.send("Searching for: " + query)

    try:
        results = []
        for result in search(query, num_results = 5):
            append = results.append(f"<{result}>")

        response = "\n" .join(results)
        await ctx.send(f"Top search results: '{query}' :\n{response}")
    except Exception as e:
        await ctx.send(f"An error occured: {str(e)}")

# Command to submit feedback
@bot.command()
async def feedback(ctx, *, message: str = None):
    if not message:
        await ctx.send("Have feedback? Just type **?feedback** and then your feedback!")
        return
    
    username = ctx.author.name
    userid = ctx.author.id

    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as file:
            lines = file.readlines()
        count = len(lines) + 1
    else:
        count = 1

    with open(feedback_file, 'a') as file:
        file.write(f"{count}. {username}: {message}\n")
        await ctx.send("Feedback submitted. Thank you!")

# Command to show socials
@bot.command()
async def links(ctx):
    embed = discord.Embed(
        title="Social Links",
        description="Here are a few links to my socials!: ",
        color=discord.Color.blue()
    )
    embed.add_field(name="LinkedIn", value="https://www.linkedin.com/in/kitryc-virak-9b5a8229a/", inline=False)
    embed.add_field(name="GitHub", value="https://github.com/kitryc", inline=False)
    embed.add_field(name="Website", value="[placeholder!]", inline=False)

    await ctx.send(embed=embed)

# Link to commands with help
@bot.command()
async def bothelp(ctx):
    embed = discord.Embed(
        title="Help",
        description="Here is a doc containing all of my commands: https://docs.google.com/document/d/1vAjbRrsTf5DtiY034MBAatYqxPHhnevBzRgJNpdCXf4/edit?tab=t.0",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Invalid Commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid Command. Use ?help or ?bothelp for a list of commands.")
    else:
        await ctx.send(f"Error occured: {str(error)}.")


#---------------------------------------------------------------------------------------END OF COMMANDS-----------------------------------==========----------------------------------------------------------------------------#
# Running Bot
bot.run('secret key')