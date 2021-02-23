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

    @commands.command(name='inspire')
    async def inspire(self, ctx):
        """Return the Quote of the day"""
        quote = get_quote()
        await ctx.send(quote)

def setup(bot):
    bot.add_cog(QODCog(bot))
