import asyncio
import os
import discord
from discord import app_commands
from discord import Intents
from discord import Client
import logging
import argparse
import config

from discord import app_commands
from dotenv import load_dotenv
from unittest.mock import patch
from transformers.dynamic_module_utils import get_imports
from transformers import AutoProcessor, AutoModelForCausalLM 
import warnings
from huggingface_hub import file_download


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

    # Command to Edit Message (You Right Click On It)
    hello_world = discord.app_commands.ContextMenu(
    name='Hello World',
    callback=hello_world,
    type=discord.AppCommandType.message
    )
    
    # Initialize the Commands
    tree.add_command(hello_world)

    await tree.sync(guild=None)  
    print(f'Discord Bot is up and running.')

@tree.command(name="hello_world", description="Say Hello World!")
async def character_list(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World~", ephemeral=True)  # Send the response


@client.event
async def on_message(message):

    if message is None:
        return
    
    # Trigger the Observer Behavior (The command that listens to Keyword)
    print("Message Get~")

# Run the Bot
client.run(discord_token)

def hello_world():

    return