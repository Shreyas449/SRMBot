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
    
    ###################
    ####ADD EMBEDS



    @app_commands.command(name="verify-outsiders",description="show all db values")
    async def verify_outsiders(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Hi, {interaction.user.mention}, please be patient a staff member will attend you soon.')
        
    

    @app_commands.command(name="verify", description="Use this command to verify, this command only verifies SRM Students.")
    async def verify(self ,interaction: discord.Interaction, mail:str):
        await interaction.response.defer(thinking=True) 
        if mail[-13::1] != "srmist.edu.in":
            await interaction.response.send_message("Sorry this command is only for verifying SRM Students. Use verify-outsiders command instead.")
            return

        ### DB check if user ID  is present in the database        
            ###nested if to check if already register user has verified role or now
        row = await self.client.get_row("user_data",key = "uid",value = interaction.user.id)
        if row != None:
            member = interaction.guild.get_member(interaction.user.id)
            roles = member.roles
            if "Verified" not in roles:
                await member.add_roles(interaction.guild.get_role(1007964811239378954))


        ### DB add row in verification_data
        uid = interaction.user.id 
        mail_to_verify = mail
        otp = random.randint(100000,1000000)
        attempts = 0
        self.client.insert_verification_data(uid,mail_to_verify,otp,attempts)

        msg = EmailMessage()
        msg['Subject'] = "SRM'26 server" 
        msg['From'] = self.client.BOT_EMAIL_ID                 
        msg['To'] =  mail_to_verify
        msg.set_content(f"Your OTP is {otp}, it will be available for another 15 minutes.")
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:

            smtp.login(self.client.BOT_EMAIL_ID,self.client.BOT_EMAIL_PASSWORD)
            smtp.send_message(msg)


        await interaction.followup.send("Check your email for the OTP and use /otp to complete verification")



    @app_commands.command(name = "otp",description="Enter OTP here after running the /verify command.")
    async def otp(self, interaction: discord.Interaction, otp:int):
        await interaction.response.defer(thinking=True)        
        ###
        # Check if user id is NOT preset in verification data
        row:dict = await self.client.get_row("verification_data",key = "uid",value = interaction.user.id)
        if row == None:                
            await interaction.followup.send("Please use the /verify command to recieve OTP first.")
            return
        if otp == row["otp"]:
            await interaction.followup.send("OTP Matched")
            member = interaction.guild.get_member(interaction.user.id)
            await member.add_roles(interaction.guild.get_role(1007964811239378954))
        else:
            tries = 3-row["attempts"] 
            await interaction.followup.send(f"OTP Not Matched, you have {tries} more tries.")
            await self.client.update_row("verification_data",{"attempts":row["attempts"]},{"attempts":row["attempts"]+1})
            row = await self.client.get_row("verification_data",key = "uid",value = interaction.user.id)
            if row["attempts"] >= 4:
                await self.client.delete_row("verification_data",key = "uid",value = interaction.user.id)
        pass



async def setup(client):
    await client.add_cog(EmailVerify(client))