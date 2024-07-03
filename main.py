import asyncio
import os

from discord import app_commands
from dotenv import load_dotenv

import apiconfig
import config
from bot.alchemy import alchemy_bot
from bot.battle import battle_bot
from bot.dungeon import dungeon_bot
from bot.dungeon import dungeon_engine
from bot.rpg import rpg_bot
from bot.rpg import rpg_engine


load_dotenv()
discord_token: str | None = os.getenv("DISCORD_TOKEN")
if discord_token is None:
    raise RuntimeError("$DISCORD_TOKEN env variable is not set!")

client = config.client

tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    # Let owner known in the console that the bot is now running!
    print(f'Discord Bot is Loading...')

    # Setup the Connection with API
    config.text_api = await apiconfig.set_api("text-default.json")
    await apiconfig.api_status_check(config.text_api["address"] + config.text_api["model"],
                                     headers=config.text_api["headers"])

    task = asyncio.create_task(rpg_engine.generate_new_player())
    task2 = asyncio.create_task(dungeon_engine.create_dungeon())

    battle_bot.setup_battle_commands(tree)
    rpg_bot.setup_rpg_commands(tree)
    dungeon_bot.setup_dungeon_commands(tree)
    #alchemy_bot.setup_alchemy_commands(tree)

    await tree.sync(guild=None)
    print(f'Discord Bot is up and running.')


# @client.event
# async def on_message(message):
#     if message is None:
#         return
#
#     # Trigger the Observer Behavior (The command that listens to Keyword)
#     print("Message Get~")


# Run the Bot
client.run(discord_token)
