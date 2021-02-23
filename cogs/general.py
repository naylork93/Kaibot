import discord
from discord.ext import commands
import random

cool_answers = [
  "Yes they are cool."
, "Actually I'll have you know they are the coolest."
, "LOL no."
, "Of course not!"
]

#make the class for the bot
class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='iscool', help='Replies if the person is cool')
    async def iscool(self, ctx, arg):
        """is the person cool?"""
        await ctx.send(arg + "? " + random.choice(cool_answers))

def setup(bot):
    bot.add_cog(GeneralCog(bot))
