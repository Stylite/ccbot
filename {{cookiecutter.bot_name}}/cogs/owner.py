import discord
from discord.ext import commands
import math
import subprocess
import textwrap

def cleanup_code(content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')


def get_syntax_error(e):
    if e.text is None:
        return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)

    return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)


class Owner:
    def __init__(self, bot):
        self.bot = bot
        self.env = {}
    

    @commands.command(hidden=True, name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        """ Evaluate Python code """
        if code == 'exit()':
            self.env.clear()
            return await ctx.send('Environment cleared')

        self.env.update({
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'guild': ctx.message.guild,
            'author': ctx.message.author,
        })

        code = code.replace('```py\n', '').replace('```', '').replace('`', '').strip()

        _code = 'async def func():\n  try:\n{}\n  finally:\n    self.env.update(locals())'\
            .format(textwrap.indent(code, '    '))

        try:
            exec(_code, self.env)

            func = self.env['func']
            output = await func()

            output = repr(output) if output else str(output)
        except Exception as e:
            output = '{}: {}'.format(type(e).__name__, e)

        code = code.split('\n')
        s = ''
        for i, line in enumerate(code):
            s += '>>> ' if i == 0 else '... '
            s += line + '\n'

        message = f'```py\n{s}\n{output}\n```'

        try:
            await ctx.send(message)
        except discord.HTTPException:
            await ctx.send('Output too large!')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, name: str):
        """ Reloads an extension in the bot """
        m = await ctx.send(f'Loading {name}')
        try:
            self.bot.unload_extension(f'cogs.{name}')
            self.bot.load_extension(f'cogs.{name}')
            await m.edit(content=f'Reloaded {name}.')
        except (ImportError, discord.ClientException) as e:
            await m.edit(content=f'Error while loading {name}.')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, name: str):
        """ Loads an extension in the bot """
        m = await ctx.send(f'Loading {name}')
        try:
            self.bot.load_extension(f'cogs.{name}')
            await m.edit(content=f'loaded {name}.')
        except (ImportError, discord.ClientException) as e:
            await m.edit(content=f'Error while loading {name}.')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, name: str):
        """ Unloads an extension in the bot """
        m = await ctx.send(f'unloading {name}')
        try:
            self.bot.unload_extension(f'cogs.{name}')
            await m.edit(content=f'Unloaded {name}.')
        except (ImportError, discord.ClientException) as e:
            await m.edit(content=f'Error while loading {name}.')



def setup(bot):
    bot.add_cog(Owner(bot))
