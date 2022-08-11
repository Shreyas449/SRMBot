import discord
from discord.ext import commands


class utility(commands.Cog):
    def __init__(self , client):
        self.client = client

    @commands.command()
    async def inrole(self,ctx,role: commands.RoleConverter):
        mems = role.members
        mem = []
        for i in role.members:
            mem.append(f"{i} ({i.id})")
        await self.client.paginate(ctx.channel,ctx.author,"Role:",raw_list=mem)

    @commands.command(aliases=["av","pfp","dp"])
    async def avatar(self,ctx , person : discord.Member = None):
        if person == None:
            person = ctx.author
        embed = discord.Embed()
        embed.set_author(name =person.name )
        embed.set_image(url = person.avatar_url)
        embed.set_footer(text=f"Requested By {ctx.author}",icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    
def setup(client):
    client.add_cog(utility(client))