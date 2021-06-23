import discord
from discord.ext import commands
from replit import db
import random

def addwatch(message):
  if "watch" in db.keys():
    watch = db["watch"]
    watch.append(message)
    db["watch"] = watch
  else:
    db["watch"] = [message]

def delwatch(index):
  watch = db["watch"]
  if len(watch) > index:
    del watch[index]
  db["watch"] = watch

#make the class for the bot
class netflixCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addwatch', help='Adds an item to the watch list')
    async def addwatch(self, ctx, *args):
        """Adds an item to the watch list"""
        text = ""
        for word in args:
          text = text + word + " "
        text = text[:-1]
        addwatch(text)
        await ctx.send(text + " added.")

    @commands.command(name='delwatch', help='Deletes an item from the watch list')
    async def delwatch(self, ctx, arg):
        """Adds an item to the watch list"""
        if arg.isdigit():
          index = int(arg)
          item = db["watch"][index]
          delwatch(index)
          await ctx.send(item + " deleted.")
        else:
          await ctx.send("Please enter the index of the item to be deleted.")

    @commands.command(name='getwatch', help='Gets the watch list')
    async def getwatch(self, ctx):
      #extract everything from the db
      #output it nicely
      output = []
      if "watch" in db.keys():
        output = db["watch"]
      await ctx.send(output)

    @commands.command(name='hitme', help='Returns a random item from the watch list')
    async def hitme(self, ctx):
      """Returns a random item from the watch list"""
      await ctx.send(random.choice(db["watch"]))

def setup(bot):
    bot.add_cog(netflixCog(bot))