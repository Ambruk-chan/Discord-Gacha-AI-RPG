from discord import app_commands
import discord
import config
from util.models import *
from util import data_manager, discordapi


#The INITS
def setup_dungeon_commands(tree: app_commands.CommandTree):

    @tree.command(name="dungeon_help", description="Show Battle Tutorial!")
    async def dungeon_help(interaction: discord.Interaction):
        dungeon_help = show_dungeon_help()
        await interaction.response.send_message(dungeon_help, ephemeral=True)

    @tree.command(name="dungeon_open", description="Open A Dungeon (For Debug)")
    async def dungeon_open(interaction: discord.Interaction, name: str):
        message = data_manager.format_dungeon_for_discord(name)
        await discordapi.send_webhook_message(interaction.channel,message)
        await interaction.response.send_message("Retrieved~")

    @tree.command(name="dungeon_create", description="Create a New Dungeon!")
    async def dungeon_create(interaction: discord.Interaction, material:str):
        config.dungeon_creation_queue.put_nowait(
            DungeonCreationQueueItem(interaction, material)
        )
        await interaction.response.send_message("Dungeon Creation in Progress~",ephemeral=True)

    @tree.command(name="dungeon_choice", description="Make a choice during encounter!")
    async def dungeon_choice(interaction: discord.Interaction):
        result = pick_choices(interaction)
        await interaction.response.send_message(result,ephemeral=True)

    @tree.command(name="dungeon_abandon", description="Abandon The Dungeon (WILL DESTROY THE DUNGEON)")
    async def dungeon_abandon(interaction: discord.Interaction):
        result = pick_abandon(interaction)
        await interaction.response.send_message(result,ephemeral=True)
    



# THE FLOWS N CHECKERS~

def show_dungeon_help():
    # This just pulls up the help menu
    return "Help Here~"

def dungeon_creation_check(data):
    # check if all is set (enough materials etc)
    # queue create dungeon
    return "Dungeon Creation in Progress~"

def pick_choices():
    # check if input is correct
    # queue "Consequences Of Thy Action" (prompt to llm)
    return "Choices Evaluation in Progress"

def pick_abandon():
    # evaluate user input
    # update user data
    # await destroy dungeon
    return "You have decided to destroy: (action)"

