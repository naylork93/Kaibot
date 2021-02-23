import discord
from discord.ext import commands
import json
import requests
import datetime
import config
import asyncio

def get_quote():
    response = requests.get("https://zenquotes.io/api/today")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

#make the class for the bot
class QODCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#        self.bg_task = self.loop.create_task(self.dailyinspire())

    @commands.command(name='inspire')
    async def inspire(self, ctx):
        """Return the Quote of the day"""
        quote = get_quote()
        await ctx.send(quote)

#    async def dailyinspire(self):
#      """Sends the inspirational quote at 8am daily to a specific channel"""
#      await self.wait_until_ready()
#      now = datetime.strftime(datetime.now(),'%H:%M')
#      channel = client.get_channel(config.INSPIRE_CHANNEL)
#      while not self.is_closed():
#        if now == config.INSPIRE_TIME:
#          quote = get_quote()
#          await channel.send(quote)
#          await asyncio.sleep(3600)

def setup(bot):
    bot.add_cog(QODCog(bot))