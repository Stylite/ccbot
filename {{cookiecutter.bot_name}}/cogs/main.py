import discord
from discord.ext import commands


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """ Gets the bots invite link """
        await ctx.send(f'Invite me using this link <{self.bot.invite_url}>')

    @commands.command()
    async def ping(self, ctx):
        """ Checks if the bot is working. """
        await ctx.send('Pong!')

    @commands.command()
    async def info(self, ctx):
        """ Gives info/credits on the bot. """
        em = discord.Embed()
        em.add_field(name="Owned by ", value="{{cookiecutter.author}}", inline=False)
        em.add_field(name="Base written by ", value=f"[senseful#0009](https://github.com/stylite/ccbot)")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Main(bot))
