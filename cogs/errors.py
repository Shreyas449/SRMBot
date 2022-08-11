import discord
from discord.ext import commands

class errors(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error,commands.CommandNotFound):
            pass 
        else: 
            print(error)


def setup(client):
    client.add_cog(errors(client))