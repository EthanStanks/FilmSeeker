import discord
from discord.ext import commands
import model
from model import tokenizer # need for model.ReadPickle()

df = model.ReadData()
tfidf_matrix, tfidf_vectorizer = model.ReadPickle()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
nums_to_recommend = 5

@bot.event
async def on_ready():
    print("FilmSeeker is now online.")
    custom_status = discord.Game("Use !info to get started!")
    await bot.change_presence(status=discord.Status.online, activity=custom_status)

@bot.command()
async def info(ctx):
    await ctx.send("List of Commands ✍️\n```!recommend 'details' - Recommends you a movie based on the details you give it. Ex: !r Batman and Superman\n!amount # - Changes the amount of recommendation you receive. Ex: !amount 3```")

@bot.command()
async def amount(ctx, user_input):
    try:
        temp = int(user_input)
        if temp > 0:
            global nums_to_recommend
            nums_to_recommend = temp
            await ctx.send(f"Now recommending {nums_to_recommend} movies.")
        else:
            await ctx.send("Please enter a number greater than 0.")
    except ValueError:
        await ctx.send("Please enter a valid number.")

@bot.command()
async def recommend(ctx, *, user_input: str):
    recommendations = model.recommend_movies(user_input,tfidf_matrix,tfidf_vectorizer,df, nums_to_recommend)
    size = len(recommendations)
    if size > 0:
        response = f"# Recommendations for: \"{user_input}\" 🎥🍿\n"
        await ctx.send(response)
        #last = size - 1
        for i, movie in enumerate(recommendations):
            movie_line = f"### {i+1}) {movie['title']}\nGenres: {movie['genres']}\nRelease Date: {movie['release_date']}\nRun Time: {movie['runtime']}\nRating: {format(movie['score'], '.2f')}\nPoster: [Poster]({movie['poster_path']})"
            await ctx.send(movie_line)
    else: 
        response = f"I can't find any recommendations for {user_input}. Please try something else."
        await ctx.send(response)

if __name__ == '__main__':
    with open('discord_token.txt', 'r') as file:
        BOT_KEY = file.read().strip()
    
    if not BOT_KEY:
        print("Failed to read bot key.")
    else:
        bot.run(BOT_KEY)
