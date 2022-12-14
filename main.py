import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
import pymongo
from discord import app_commands



### MAIN BOT CLASS ###
load_dotenv()
class SRMBot(commands.Bot):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.OWNERS = [384643376055844864,759817307957493800,528856976432693259]
        self.TEST_GUILD = 908203872454062111
        self.BOT_EMAIL_ID = os.getenv('BOT_EMAIL_ID')
        self.BOT_EMAIL_PASSWORD = os.getenv("BOT_EMAIL_PASSWORD")
        self.MONGODB_USER = os.getenv("MONGODB_USER")
        self.MONGODB_PASS = os.getenv("MONGODB_PASS")

        self.COLOUR = 0x0c4da2

        # set-up for mongo db atlas
        # connection string to be used for connection to mongodb atlas 
        self.connectionString = f"mongodb+srv://{self.MONGODB_USER}:{self.MONGODB_PASS}@cluster0.jk7ns7p.mongodb.net/?retryWrites=true&w=majority"

 
        self.db_client = pymongo.MongoClient(self.connectionString)      # connecting to the database

    # creating a database named srm_bot_database --> if the database already exist then it will connect to it directly
        self.db = self.db_client['srm_bot_database']

    # creating a collection
        self.user_data = self.db.user_data     # collection for verified users (user_data)
        self.verification_data = self.db.verification_data      # collection to be used for verifing user (verification_data)

    # use to insert data into the user_data collection --> this is the main collection where verified users data gets stored
    # refined data storage here
    async def insert_user_data(self,uid,stu_mail):
        user_data = {
            "uid": uid,
            "stu_mail": stu_mail
        }
        user_id = self.user_data.insert_one(user_data).inserted_id
        print(f"student with: \ninserted_id: {user_id} \nuid: {uid} \nstud_mail: {stu_mail} \nhas been verified and created!")

    # use this to insert data into the verification_data collection --> this is the temporary data collection where all the data gets stored
    # raw data storage here
    async def insert_verification_data(self,uid, mail_id, otp, attemps):
        raw_data = {
            "uid": uid,
            "mail_id": mail_id,
            "otp": otp,
            "attempts": attemps
        }
        unverified_user_id = self.verification_data.insert_one(raw_data).inserted_id
        print(f"unverified user with id {unverified_user_id} has been created!")

    async def get_row(self,collection,key = None,value = None):
        if collection == "user_data":
            if key == None:
                row = self.user_data.find_one()
            else:
                row = self.user_data.find_one({key:value})
        elif collection == "verification_data":
            if key == None:
                row = self.verification_data.find_one()
            else:
                row = self.verification_data.find_one({key:value})                         
        return row
    
    async def delete_row(self,collection,key = None,value = None):
        if collection == "user_data":
            if key == None:
                row = self.user_data.delete_one()
            else:
                row = self.user_data.delete_one({key:value})
        elif collection == "verification_data":
            if key == None:
                row = self.verification_data.delete_one()
            else:
                row = self.verification_data.delete_one({key:value})                         
        return row

    async def update_row(self,collection,old_value,new_value):        
        if collection == "user_data":
            self.user_data.update_one(old_value,{"$set":new_value})
        elif collection == "verification_data":
            self.verification_data.update_one(old_value,{"$set":new_value})

    #############################################

    async def setup_hook(self):
        self.tree.copy_global_to(guild=discord.Object(self.TEST_GUILD))
        await self.tree.sync(guild=discord.Object(self.TEST_GUILD))

    def _member_count(self):
        m = 0
        for guilds in self.guilds:
            m += guilds.member_count
        return m

    async def on_ready_but_once(self):
        await self.wait_until_ready()
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded {filename[:-3]}")
        print("Loaded All Cogs") 

        await self.setup_hook()       

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
        for i in ["??????","??????","??????"]:
            await msg.add_reaction(i)

        def react_check(reaction,user):
            return reaction.message == msg and caller == user and reaction.emoji in ["??????","??????","??????"]

        # print(list)
        while True:
            reaction,user = await self.wait_for("reaction_add", timeout=30, check=react_check)
            await msg.remove_reaction(reaction.emoji,user)
            try:
                if reaction.emoji == "??????":
                    page +=1
                    # print("Add1",page) 
                    if page >= max_page:
                        page = 0
                    # print("Add2",page)
                elif reaction.emoji == "??????":
                    page-=1
                    # print("Back1",page)
                    if page <= -(max_page):
                        page = max_page
                    # print("Back2",page)
                elif reaction.emoji == "??????":
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
    await client.load_extension("jishaku")

@client.command()
@is_admin()
async def load(ctx, extention):
    await client.load_extension(f"cogs.{extention}")

@client.command()
@is_admin()
async def unload(ctx, extention):
    await client.unload_extension(f"cogs.{extention}")

@client.command()
@is_admin()
async def reload(ctx, extention):
    await client.reload_extension(f"cogs.{extention}")

@client.command()
@is_admin()
async def logout(ctx):
    await ctx.send("Bot Logging Out, ByeBye!????")
    await client.close()

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


client.run(TOKEN)