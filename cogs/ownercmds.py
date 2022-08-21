import discord
from discord.ext import commands
from discord import app_commands


class ownercmds(commands.Cog):
    def __init__(self , client):
        self.client = client

    @app_commands.command(name="show",description="show all db values")
    async def show(self, interaction: discord.Interaction):
        row = await self.client.get_row("verification_data")
        await interaction.response.send_message(f" Hi, {row}")
    
    @app_commands.command(name="temp",description="show all db values")
    async def temp(self, interaction: discord.Interaction):
        role = member = discord.utils.find(lambda m: m.name == 'Verified', interaction.guild.roles)
        await interaction.response.send_message(f" Hi, <@&{role.id}>")
    
async def setup(client):
    await client.add_cog(ownercmds(client))