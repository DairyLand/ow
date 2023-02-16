import asyncio
import os
import random
import discord
from discord.ext import commands
from discord_components.client import DiscordComponents
from discord import Embed
import asyncpraw
from random import random

bot = commands.Bot(command_prefix='$')
ownerid = []
botowner = 'ThiccDaddy#1750'
bot.remove_command('help')


reddit = asyncpraw.Reddit(client_id='WirWugQJMWZrR8GsZGosEg',
                          client_secret='ZGaCRxEl0OBrVdbeti_6Xn81YUXYlg',
                          username='No-Giraffe-691',
                          password='fakepass',
                          user_agent='ow_bot'
                          )


all_subs = []


async def gen_memes():
    subreddit = await reddit.subreddit('Overwatch_Memes')
    top = subreddit.top(limit=500)
    async for submission in top:
