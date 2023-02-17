import discord
from discord import Embed
from discord.ext import commands
import asyncpraw
import random
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


import os
import random
import discord
from discord.ext import commands
import asyncpraw
import async_timeout
import aiohttp


intents = discord.Intents.all()


bot = commands.Bot(command_prefix='$', intents=intents)
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


async def gen_memes(client_id, client_secret, username, password, user_agent):
    async with aiohttp.ClientSession() as session:
        reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent,
        )
        subreddit = await reddit.subreddit("memes")
        top = subreddit.top(limit=50, time_filter="day")
        try:
            async for submission in top:
                async with session.get(submission.url) as resp:
                    if resp.status != 200:
                        continue
                    await send_meme(submission.url, submission.title)
        except asyncprawcore.exceptions.RequestException:
            print("RequestException occurred. Retrying in 5 seconds.")
            await asyncio.sleep(5)
            await gen_memes(client_id, client_secret, username, password, user_agent)




@bot.event
async def on_ready():
    print('Fired up & ready!')
    await gen_memes()


@bot.command(aliases=['memes'])
async def meme(ctx):
    if not all_subs:
        await gen_memes()

    random_sub = random.choice(all_subs)
    all_subs.remove(random_sub)
    name = random_sub.title
    url = random_sub.url
    likes = random_sub.score
    comments = random_sub.num_comments
    link = random_sub.permalink

    embed = discord.Embed(title=f'__{name}__', colour=discord.Colour.random(),
                          timestamp=ctx.message.created_at, url=f'https://reddit.com{link}')
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_image(url=url)
    embed.set_footer(text=f'👍{likes} 💬{comments}',
                     icon_url='https://www.vectorico.com/download/social_media/Reddit-Icon.png')
    await ctx.send(embed=embed)


@bot.command(name='reload-meme')
async def reload_meme(ctx):
    msg = await ctx.send('Reloading memes ...')
    await gen_memes()
    await msg.edit(content='Great success! ✅')
