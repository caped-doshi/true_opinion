import discord
from discord.ui import Button, View
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
from FuzzySeach import SearchAlgorithm
load_dotenv()

bot = discord.Bot()
uri = getenv('uri')

client = AsyncIOMotorClient(uri)
db = client.get_database("ratings")
collection = db.get_collection("imdb")

class button_imdb(Button):
    async def callback(self, interaction):
        c = "Hello " + str(interaction.user)
        c += ", here are the results for " + "**" + self.label + "**" + "\n"
        imdb_rating = await find_by_id(self.label)
        c += "**IMDB rating: " + imdb_rating['imdb'] + "**"
        await interaction.response.edit_message(content=c, view=None)

class button_rt(Button):
    async def callback(self, interaction):
        c = "Hello " + str(interaction.user)
        c += ", here are the results for " + "**" + self.label + "**" + "\n"
        imdb_rating = await find_by_id(self.label)
        c += "**Rotten Tomatoes rating: " + imdb_rating['rt'] + "**"
        await interaction.response.edit_message(content=c, view=None)


async def find_by_id(id):
    cursor = await collection.find_one({'_id':id})
    return cursor

@bot.slash_command(guild_ids=[748940193733804252])
async def hello(ctx, name):
    await ctx.respond('Hello ' + name)

@bot.slash_command(name='add', guild_ids=[748940193733804252])
async def add(ctx, num1: int, num2: int):
    await ctx.respond(num1 + num2)

@bot.slash_command(guild_ids=[748940193733804252])
async def ping(ctx):
    await ctx.respond('pong')

@bot.slash_command(name='imdb',guild_ids=[748940193733804252])
async def imdb_result(ctx, query: str):
    ctx.defer()
    movies_arr = await find_by_id('all_movies')
    algo = SearchAlgorithm(movies_arr['arr'])
    top_5_arr = await algo.top_5(query)
    button1 = button_imdb(label=top_5_arr[0],style=discord.ButtonStyle.primary,
     emoji="✔")
    button2 = button_imdb(label=top_5_arr[1],style=discord.ButtonStyle.primary,
     emoji="✔")
    button3 = button_imdb(label=top_5_arr[2],style=discord.ButtonStyle.primary,
     emoji="✔")
    
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    await ctx.respond("Top 3 Results for your search: ",view=view)

@bot.slash_command(name='rotten_tomatoes',guild_ids=[748940193733804252])
async def imdb_result(ctx, query: str):
    movies_arr = await find_by_id('all_movies')
    algo = SearchAlgorithm(movies_arr['arr'])
    top_5_arr = await algo.top_5(query)
    button1 = button_rt(label=top_5_arr[0],style=discord.ButtonStyle.primary,
     emoji="✔")
    button2 = button_rt(label=top_5_arr[1],style=discord.ButtonStyle.primary,
     emoji="✔")
    button3 = button_rt(label=top_5_arr[2],style=discord.ButtonStyle.primary,
     emoji="✔")
    
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    await ctx.respond("Top 3 Results for your search: ",view=view)


@bot.slash_command(name='all_movies', guild_ids=[748940193733804252])
async def all_movies(ctx):
    await ctx.defer()
    arr = await find_by_id('all_movies')
    length = len(arr['arr'])
    await ctx.respond(f"There are a total of **{length}** movies in the database")

bot.run(getenv('TOKEN'))

