import discord
from discord.ext import commands
import model
from model import tokenizer # need for model.ReadPickle()

df = model.ReadData()
tfidf_matrix, tfidf_vectorizer = model.ReadPickle()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("FilmSeeker is now online.")
    custom_status = discord.Game("Use !info to get started!")
    await bot.change_presence(status=discord.Status.online, activity=custom_status)

@bot.command()
async def info(ctx):
    await ctx.send("List of Commands: Coming Soon!")

@bot.command()
async def r(ctx, *, user_input: str):
    recommendations = model.recommend_movies(user_input,tfidf_matrix,tfidf_vectorizer,df)
    size = len(recommendations)
    if size > 0:
        response = f"I recommend these movies for: {user_input}\n"
        await ctx.send(response)
        #last = size - 1
        for i, movie in enumerate(recommendations):
            movie_line = f"{i+1}) {movie['title']}\nGenres: {movie['genres']}\nRelease Date: {movie['release_date']}\nRun Time: {movie['runtime']}\nRating: {movie['score']}\nPoster: {movie['poster_path']}"
            await ctx.send(movie_line)
            #response += movie_line
            #if i is not last:
                #response += "\n------------------------------------------------------------\n"
    else: 
        response = f"I can't find any recommendations for: {user_input}. Please try something else."
        await ctx.send(response)

if __name__ == '__main__':
    with open('discord_token.txt', 'r') as file:
        BOT_KEY = file.read().strip()
    
    if not BOT_KEY:
        print("Failed to read bot key.")
    else:
        bot.run(BOT_KEY)
