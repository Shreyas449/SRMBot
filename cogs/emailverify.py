import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import smtplib
from email.message import EmailMessage



class EmailVerify(commands.Cog):
    def __init__(self , client):
        self.client = client
        
    @app_commands.command(name="command-1")
    async def my_command(self, interaction: discord.Interaction):
        """Command 1"""
        await interaction.response.send_message(f'Hi, {interaction.user.mention}')
    

    @app_commands.command(name="verify", description="Use this command to verify, this command only verifies SRM Students.")
    async def verify(self ,interaction: discord.Interaction, mail:str):

        # if mail[-13::1] != "srmist.edu.in":
        #     await interaction.response.send_message("Sorry this command is only for verifying SRM Students. Use ____ command.")
        #     return

        ### DB check if user ID  is present in the database        
            ###nested if to check if already register user has verified role or now

        ### DB add row in verification_data

        print(interaction.user.id)
        
        uid = interaction.user.id 
        mail_to_verify = mail
        otp = random.randint(100000,1000000)
        attempts = 0
        
        await interaction.response.send_message("Check your email for the OTP and use /otp to complete verification")


        # msg = EmailMessage()
        # msg['Subject'] = "SRM'26 server" 
        # msg['From'] = self.client.BOT_EMAIL_ID                 
        # msg['To'] =  mail_to_verify
        # msg.set_content(f"Your OTP is {otp}, it will be available for another 15 minutes.")
        # with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:

        #     smtp.login(self.client.BOT_EMAIL_ID,self.client.BOT_EMAIL_PASSWORD)
        #     smtp.send_message(msg)


        await interaction.response.send_message("Check your email for the OTP and use /otp to complete verification")

        # await asyncio.sleep(60*5)


    @app_commands.command(name = "otp",description="Enter OTP here after running the /verify command.")
    async def otp(self, interaction, otp:int):
                
        ###
        # Check if user id is NOT preset in verification data
        # if interaction.user.id not in                 
            # interaction.response.send_message("Please use the /verify command to recieve OTP first.")
        pass


async def setup(client):
    await client.add_cog(EmailVerify(client))