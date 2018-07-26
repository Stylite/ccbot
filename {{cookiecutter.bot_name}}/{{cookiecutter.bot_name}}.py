from discord.ext import commands
import os
import json

with open('config.json') as config:
    config = json.load(config)

bot = commands.AutoShardedBot(command_prefix=config['prefix'], description = """{{cookiecutter.description}}""")

for cog in os.listdir('cogs'):
    if not cog.endswith('.py'):
        continue
    try:
        bot.load_extension(f'cogs.{cog[:-3]}')
    except SyntaxError as es:
        print(f'Failed to load cog {cog} becayse of a syntaxerror.')
    except ImportError as ei:
        print(f'Failed to load {cog} because of a importerror.')

    @bot.event
    async def on_message(ctx):
        if not bot.is_ready() or ctx.author.bot:
            return

        await bot.process_commands(ctx)

    @bot.event
    async def on_ready():
        print('Login successful.')
        print(f'Logged in as: {bot.user.name}')
        print(f'Server count: {len(bot.guilds)}')

bot.run(config['token'])