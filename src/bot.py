import discord
from discord.ext import commands
import model
from model import tokenizer # need for model.ReadPickle()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("FilmSeeker is now online.")
    custom_status = discord.Game("Use !info to get started!")
    await bot.change_presence(status=discord.Status.online, activity=custom_status)

@bot.command()
async def info(ctx):
    await ctx.send("List of Commands: Coming Soon!")

if __name__ == '__main__':
    with open('discord_token.txt', 'r') as file:
        BOT_KEY = file.read().strip()
    
    if not BOT_KEY:
        print("Failed to read bot key.")
    else:
        tfidf_matrix, tfidf_vectorizer = model.ReadPickle()
    
        bot.run(BOT_KEY)
