import os
import traceback
import json

from discord.ext import commands

with open('config.json') as config:
    config = json.load(config)

bot = commands.AutoShardedBot(
        command_prefix=config['prefix'],
        description = """{{cookiecutter.description}}"""
)

for cog in os.listdir('cogs'):
    if not cog.endswith('.py'):
        continue
    try:
        bot.load_extension(f'cogs.{cog[:-3]}')
    except Exception as e:
        stack_trace =  "".join(traceback.format_exception(
                            type(e),
                            e,
                            e.__traceback__
                        ))
        print(f"Failed to load cog {cog}, stack trace:\n{stack_trace}")
    else:
        print(f"Successfully loaded cog {cog}!")


    @bot.event
    async def on_message(ctx):
        if not bot.is_ready() or ctx.author.bot:
            return

        await bot.process_commands(ctx)

    @bot.event
    async def on_ready():
        print('Login successful.')
        print(f'Logged in as: {bot.user.name}')
        print(f'Bot ID: {bot.user.id}')
        print(f'Server count: {len(bot.guilds)}')

bot.run(config['token'])
