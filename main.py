import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv



### MAIN BOT CLASS ###

class SRMBot(commands.Bot):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.OWNERS = [384643376055844864,759817307957493800,528856976432693259]
        # self.db = mysql.connector.connect(
        # host="localhost",
        # user = "root",
        # passwd = "root",
        # database = "srmbot"
        # )
        # self.c = self.db.cursor(buffered=True)


    def _member_count(self):
        m = 0
        for guilds in self.guilds:
            m += guilds.member_count
        return m

    async def on_ready_but_once(self):
        await self.wait_until_ready()
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded {filename[:-3]}")
        print("Loaded All Cogs")        

    async def paginate(self,
    channel,
    caller,
    title=None,
    description="",
    footer=None,
    thumbnail=None,
    raw_list=[]):
        page=0
        list = []
        x = 0
        colour = discord.Colour.random()
        for i in range(0,len(raw_list)+1,20):
            str = "\n".join(raw_list[x:x+20])
            x +=20
            list.append(str)
        max_page=len(list)

        e = discord.Embed(
            title=title,
            description=f"{description}\n {list[page]}",
            colour= colour
        )
        e.set_footer(text=f"Page {page+1}/{max_page}")
        e.set_thumbnail(url=channel.guild.icon_url)        
        msg = await channel.send(embed=e)
        for i in ["◀️","⏹️","▶️"]:
            await msg.add_reaction(i)

        def react_check(reaction,user):
            return reaction.message == msg and caller == user and reaction.emoji in ["◀️","⏹️","▶️"]

        # print(list)
        while True:
            reaction,user = await self.wait_for("reaction_add", timeout=30, check=react_check)
            await msg.remove_reaction(reaction.emoji,user)
            try:
                if reaction.emoji == "▶️":
                    page +=1
                    # print("Add1",page) 
                    if page >= max_page:
                        page = 0
                    # print("Add2",page)
                elif reaction.emoji == "◀️":
                    page-=1
                    # print("Back1",page)
                    if page <= -(max_page):
                        page = max_page
                    # print("Back2",page)
                elif reaction.emoji == "⏹️":
                    raise Exception 


                new_page= discord.Embed(
                    title=title,
                    description=f"{description}\n {list[page]}",
                    colour= colour
                )
                new_page.set_footer(text=f"Page {page+1}/{max_page}")
                new_page.set_thumbnail(url=channel.guild.icon_url)
                await msg.edit(embed=new_page)
            except Exception as e:
                # print(e)
                await msg.clear_reactions()

async def get_prefix(client,message):
    p = ["+",f'<@{client.user.id}> ', f'<@!{client.user.id}> ']
    # get = await client.fetch_from_db(message.guild.id,"general","prefix")
    # p.extend(get)

    if message.author.id in client.OWNERS :
        p.extend([""])
    
    return p


# Initializing the bot object 
client = SRMBot(command_prefix = get_prefix ,intents=discord.Intents.all(), case_insensitive = True)

### ENV VARIABLES ###
load_dotenv()

TOKEN  = os.getenv("TOKEN")

def is_admin():
    def predicate(ctx):
        if ctx.author.id in client.OWNERS:
            return True
        return False
    return commands.check(predicate)

@client.event
async def on_connect():
    client.loop.create_task(client.on_ready_but_once())
    print(f"Logged In As {client.user.name}")
    client.load_extension("jishaku")

@client.command()
@is_admin()
async def load(ctx, extention):
    client.load_extension(f"cogs.{extention}")

@client.command()
@is_admin()
async def unload(ctx, extention):
    client.unload_extension(f"cogs.{extention}")

@client.command()
@is_admin()
async def reload(ctx, extention):
    client.reload_extension(f"cogs.{extention}")

@client.command()
@is_admin()
async def logout(ctx):
    await ctx.send("Bot Logging Out, ByeBye!👋")
    await client.logout()

client.run(TOKEN)