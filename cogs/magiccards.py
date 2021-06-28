from discord.ext import commands
import sqlite3
import asyncio

def add_db():
    conn = sqlite3.connect('magiccards.db')
    c = conn.cursor()
    with conn:
        c.execute("""CREATE TABLE magiccards (
                amount INTEGER,
                name TEXT,
                foil TEXT
                )""")

def add_card(amount, name, foil):
    conn = sqlite3.connect('magiccards.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO magiccards VALUES (:amount, :name, :foil)",
        {'amount': amount, 'name': name, 'foil': foil}
        )

def get_all_cards():
    conn = sqlite3.connect('magiccards.db')
    c = conn.cursor()
    c.execute("SELECT name, amount, foil FROM magiccards ORDER BY name")
    values = c.fetchall()
    long_string = len(max(values, key=lambda t: len(t[0]))[0])
    titles = ('Name', 'Amount', 'Foil')
    table = [titles] + values
    output = ''
    for i, d in enumerate(table):
        line = '|'.join(str(x).ljust(long_string + 4) for x in d)
        output = output + '\n' + line
    
    return "```" + output + "```"

def get_card(name):
    conn = sqlite3.connect('magiccards.db')
    c = conn.cursor()
    c.execute("SELECT name, amount, foil FROM magiccards WHERE name LIKE :name",
        {'name': '%' + name + '%'}
        )
    values = c.fetchall()
    long_string = len(max(values, key=lambda t: len(t[0]))[0])
    titles = ('Name', 'Amount', 'Foil')
    table = [titles] + values
    output = ''
    for i, d in enumerate(table):
        line = '|'.join(str(x).ljust(long_string + 4) for x in d)
        output = output + '\n' + line
    
    return "```" + output + "```"

def update_amount(amount, name):
    conn = sqlite3.connect('magiccards.db')
    c = conn.cursor()
    with conn:
        c.execute("UPDATE magiccards SET amount = :amount WHERE name = :name",
        {'amount': amount, 'name': name}
        )

def update_foil(foil, name):
    conn = sqlite3.connect('magiccards.db')
    c = conn.cursor()
    with conn:
        c.execute("UPDATE magiccards SET foil = :foil WHERE name = :name",
        {'foil': foil, 'name': name}
        )

def delete_card(name):
    conn = sqlite3.connect('magiccards.db')
    c = conn.cursor()
    with conn:
        c.execute("DELETE FROM magiccards WHERE name = :name",
        {'name': name}
        )

def delete_all_cards():
    conn = sqlite3.connect('magiccards.db')
    c = conn.cursor()
    with conn:
        c.execute("DELETE FROM magiccards")

def transform_name(*name):
    cardname =""
    for word in name:
       cardname = cardname + word + " "
    cardname = cardname[:-1]
    return cardname.title()

class Magiccards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='addcard', help='Adds a card to the database specifying amount, name and optional foil (y/n)')
    async def addcard(self, ctx, amount, *name):

        await ctx.send("Should this be foil? (y/n)")
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content.lower() in ["y", "n"]

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=15)
            if msg.content.lower() == "y":
                foil = 'Y'
            else:
                foil = 'N'
        except asyncio.TimeoutError:
            foil = 'N'

        cardname = transform_name(*name)
        add_card(amount, cardname, foil)
        await ctx.send("Card '{}' has been added. Amount = '{}', Foil = '{}'".format(cardname, amount, foil)) 

    @commands.command(name='getcard', help='Gets a particular card')
    async def getcard(self, ctx, *name):
        cardname = transform_name(*name)
        output = get_card(cardname)
        await ctx.send(output)

    @commands.command(name='getallcards', help='Returns all cards')
    async def getallcards(self, ctx):
        output = get_all_cards()
        await ctx.send(output)

    @commands.command(name='updateamount', help='Updates the amount on a card')
    async def updateamount(self, ctx, amount, *name):
        cardname = transform_name(*name)
        update_amount(amount, cardname)
        output = get_card(cardname)
        await ctx.send(output)

    @commands.command(name='updatefoil', help='Updates the foil of a card')
    async def updatefoil(self, ctx, foil, *name):
        cardname = transform_name(*name)
        update_foil(foil, cardname)
        output = get_card(cardname)
        await ctx.send(output)

    @commands.command(name='deletecard', help='Deletes a card')
    async def deletecard(self, ctx, *name):
        cardname = transform_name(*name)
        delete_card(cardname)
        await ctx.send(cardname + " has been deleted.")

    @commands.command(name='deleteallcards', help='Deletes all cards')
    async def deleteallcards(self, ctx,):
        delete_all_cards()
        await ctx.send("All cards have been deleted.")

def setup(bot):
    bot.add_cog(Magiccards(bot))
    #add_db()




