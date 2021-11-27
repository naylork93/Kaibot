from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests
import config
import asyncio
import datetime

def get_epicgames():
    #set the URL to the website we want to scrape
    URL = 'https://www.pcgamer.com/epic-games-store-free-games-list/'

    #get the page
    page = requests.get(URL)

    #parse the page
    soup = BeautifulSoup(page.content, 'html.parser')

    #extract just the article body
    article_body = soup.find(id='article-body')

    #The strong tag represents the date, so find the entire set of tags it is enclosed in as this will contain the games for the week
    this_week = article_body.strong.previous_element

    #Print the date from the strong tag
    output = article_body.find('strong').contents[0] + "\n"

    #Find all the a tags which contain the game info
    #Using find all because some weeks have multiple
    freegames = this_week.find_all('a', {"data-url" : True})
    #Loop over each game
    for game in freegames:
        name = game.contents[0]
        link = game.get('href')

        output = output + name + "\n" + link + "\n"
    
    return(output)


#make the class for the bot
class Gaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weeklyepic.start()

    @commands.command(name='getfreegames')
    async def getfreegames(self, ctx):
        """Gets the current free games on the epic games store"""
        games = get_epicgames()
        await ctx.send(games)

    @tasks.loop(hours=168)
    async def weeklyepic(self):
      """Gets the weekly free games from the epic games store"""
      games = get_epicgames()
      channel = await self.bot.fetch_channel(config.EPICGAMES_CHANNEL)
      await channel.send(games)

    @weeklyepic.before_loop
    async def before_weeklyepic(self):
      for _ in range(60*60*24):
        if int(datetime.datetime.now().strftime("%w")) == config.EPICGAMES_DAY \
        and datetime.datetime.now().hour == config.EPICGAMES_TIME:
            print('Run the weekly epic')
            return
        await asyncio.sleep(3600)


def setup(bot):
    bot.add_cog(Gaming(bot))