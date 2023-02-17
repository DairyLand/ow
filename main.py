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
        all_subs.append(submission)


@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    print('Fired up & ready!')
    DiscordComponents(bot)
    await gen_memes()


@bot.command(aliases=['memes'])
async def meme(ctx):
    random_sub = random.choice(all_subs)
    all_subs.append(random_sub)
    name = random_sub.title
    url = random_sub.url
    likes = random_sub.score
    comments = random_sub.num_comments
    link = random_sub.permalink

    embed = Embed(title=f'__{name}__', colour=discord.Colour.random(
    ), timestamp=ctx.message.created_at, url=f'https://reddit.com{link}')
    embed.set_author(name=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)
    embed.set_image(url=url)
    embed.set_footer(text=f'👍{likes} 💬{comments}',
                     icon_url='https://www.vectorico.com/download/social_media/Reddit-Icon.png')
    await.ctx.send(embed=embed)

    if len(all_subs) <= 20:
        await gen_memes()


@bot.command(name='reload-meme')
async def reload_meme(ctx):
    msg = await ctx.send('Reloading memes ...')
    await gen_memes()
    await msg.edit(content='Great success! ✅')
