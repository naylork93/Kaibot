from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests

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

    @commands.command(name='getfreegames')
    async def getfreegames(self, ctx):
        """Gets the current free games on the epic games store"""
        games = get_epicgames()
        await ctx.send(games)


def setup(bot):
    bot.add_cog(Gaming(bot))