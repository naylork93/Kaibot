import discord
from discord.ext import commands, tasks
import json
import requests
import datetime
import config
import asyncio
import os

def get_quote():
    response = requests.get("https://zenquotes.io/api/today")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

#make the class for the bot
class QuoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dailyinspire.start()

    @commands.command(name='inspire')
    async def inspire(self, ctx):
        """Return the Quote of the day"""
        quote = get_quote()
        await ctx.send(quote)

    @tasks.loop(hours=24)
    async def dailyinspire(self):
      """Sends the inspirational quote at 8am daily to a specific channel"""
      quote = get_quote()
      channel = await self.bot.fetch_channel(config.INSPIRE_CHANNEL)
      await channel.send(quote)

    @dailyinspire.before_loop
    async def before_daily(self):
      for _ in range(60*60*24):  # loop the whole day
        if datetime.datetime.now().hour == 8:  # 24 hour format
            print('It is time')
            return
        await asyncio.sleep(3600)

def setup(bot):
    bot.add_cog(QuoteCog(bot))