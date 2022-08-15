import discord
from discord.ext import commands
from discord import app_commands
import logging
import random
import math
import smtplib
from email.message import EmailMessage
import mysql.connector

db = mysql.connector.connect(
    host= "localhost",
    user = "root",
    auth_plugin='mysql_native_password',
    db = "srm_discord_email_verifier"
    )
mycursor = db.cursor()

logging.basicConfig(filename="log_for_srm_bot.log",format="%(message)s, %(asctime)s  ", filemode="a",datefmt="%d/%m/%Y %I:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

bot  = commands.Bot(command_prefix="/", intents=discord.Intents.all())
token = ""

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=908203872454062111))
        self.synced = True
        print("Bot is online !!")


bot = abot()
tree = app_commands.CommandTree(bot)

######### 1 #########
@tree.command(name="verify",description="Verifies you into the server (sends otp)",guild=discord.Object(id=908203872454062111))
async def new(interation: discord.Interaction, mail:str):
    await interation.response.send_message(f"Hi {interation.user}. Sending your mail..")
    try:
        digits="0123456789"
        OTP=""
        for i in range(6):
            OTP+=digits[math.floor(random.random()*10)]
        otp = OTP 
        msg= otp
        Sender_Email = "verifyyourmail2324@gmail.com"
        Reciever_Email = mail
        # if "@srmist.edu.in" in mail:
        mail_ini = mail.split("@")
        nam = str(interation.user)
        id_nam = interation.user.id
        Password = ""
        add_details = ("INSERT INTO mailverifier "
                "(name_id,name, email, otp) "
                "VALUES (%s, %s, %s, %s)")
        data_details= (id_nam,nam,mail_ini[0],otp)              
        mycursor.execute(add_details,data_details)
        db.commit()  
        newMessage = EmailMessage()                         
        newMessage['Subject'] = "SRM'26 server" 
        newMessage['From'] = Sender_Email                   
        newMessage['To'] = Reciever_Email                   
        newMessage.set_content(f'Here is your otp, use it to verify {msg}') 

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            
            smtp.login(Sender_Email, Password)              
            smtp.send_message(newMessage)
        await interation.followup.send('''OTP sent !! Check your mail
    now use /otp command to verify yourself''')
    except:
        await interation.followup.send("Mail NOT sent, contact dev team :(")
        logger.error(f"mail not sent to {interation.user}")
    # else: 
        # await interation.response.send_message("Wrong mail!!")


######### 2 #########
@tree.command(name="otp",description="Verifies you into the server(enter otp) ",guild=discord.Object(id=908203872454062111))
async def new(interation: discord.Interaction,mail:str,otp:int):
    # if "@srmist.edu.in" in mail:
        role = "verified"
        mail_ini = mail.split("@")
        query_ini = ("select otp from mailverifier where email ='%s'"%mail_ini[0])
        mycursor.execute(query_ini)
        fin_otp = mycursor.fetchone()
        if fin_otp[0]==otp:
        
            update_table = ("""UPDATE mailverifier 
                        SET verified = %s
                        WHERE email = '%s' and otp = %s """)
            mycursor.execute(update_table%(1,mail_ini[0],otp))    
            db.commit()                   
            await interation.response.send_message("Verified, you have been given your verified role too :) ")
            try:
                await interation.user.add_roles(discord.utils.get(interation.user.guild.roles, name=role))
            except:
                await interation.followup.send("contact the dev team if you r not given the verified role..") 
                logger.error(f"role not given to {interation.user}") 
        else:
            await interation.response.send_message("not verified")
    # else:
    #     await interation.response.send_message("Wrong mail!!")        

    
bot.run(token)