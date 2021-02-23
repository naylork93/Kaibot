import discord
from discord.ext import commands
import sys, traceback
import config
from keep_alive import keep_alive

#define the prefixes used to call the bot
def get_prefix(bot, message):
    prefixes = ['!']

    return commands.when_mentioned_or(*prefixes)(bot,message)

#define our bot
bot = commands.Bot(command_prefix=get_prefix, description='KaiBot')

if __name__ == '__main__':
    for extension in config.COGS_LIST:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')

keep_alive()
bot.run(config.TOKEN, bot=True, reconnect=True)