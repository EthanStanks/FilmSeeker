import discord
from discord.ext import commands
import pickle
import model

BOT_KEY = 'bot_key'

with open('data/tfidf_matrix.pkl', 'rb') as file:
        tfidf_matrix = pickle.load(file)
with open('data/tfidf_vectorizer.pkl', 'rb') as file:
        tfidf_vectorizer = pickle.load(file)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("FilmSeeker is now online.")
    custom_status = discord.Game("Use !info to get started!")
    await bot.change_presence(status=discord.Status.online, activity=custom_status)

@bot.command()
async def info(ctx):
    await ctx.send("List of Commands: Coming Soon!")

# todo create command for movie recommendations

bot.run(BOT_KEY)