import discord
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

@bot.slash_command(name='search',guild_ids=[748940193733804252])
async def search_result(ctx, query: str):
    movies_arr = await find_by_id('all_movies')
    algo = SearchAlgorithm(movies_arr['arr'])
    top_5_arr = await algo.top_5(query)
    await ctx.respond("These are your top 5 results from your search: " + ", ".join(top_5_arr))

@bot.slash_command(name='all_movies', guild_ids=[748940193733804252])
async def all_movies(ctx):
    arr = await find_by_id('all_movies')
    string = " ".join(arr['arr'])
    await ctx.respond('All Movies in database: ' + string)

bot.run(getenv('TOKEN'))

