from ast import Delete
import discord
from discord.ext import commands


class SSVerify(commands.Cog):
    def __init__(self , client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.attachments is None:
            await message.channel.send("Please Attach The Required Screenshot",delete_after = 5)
            await message.delete()
        else: 
            ch = self.client.fetch_channel(1001132117255786517)
            await ch.send(message.attachments)



def setup(client):
    client.add_cog(SSVerify(client))