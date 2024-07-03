import asyncio
import discord
from discord import app_commands
import config
from bot.rpg import rpg_engine
from util.models import *


def setup_rpg_commands(tree: app_commands.CommandTree):
    group = app_commands.Group(name="rpg", description="RPG Commands!!!")

    @group.command(name="begin", description="Begin Your Story!!!")
    async def rpg_stat(interaction: discord.Interaction):
        # Pull up character creation modal
        await interaction.response.send_modal(CharacterCreatorModal())

    @group.command(name="equipment", description="Show your current Equipment!")
    async def rpg_equipment(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"RPG Equipment Triggered!", ephemeral=True)

    @group.command(name="player", description="Show your current Persona!")
    async def rpg_player(interaction: discord.Interaction):
        player_info = rpg_engine.getPlayerInfo(interaction.user.display_name)
        await interaction.response.send_message(player_info, ephemeral=True)

    @group.command(name="item", description="Show your current materialss!")
    async def rpg_item(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"RPG Item Triggered!", ephemeral=True)

    tree.add_command(group)


class CharacterCreatorModal(discord.ui.Modal, title='Create Character'):
    description = discord.ui.TextInput(label="About Yourself", placeholder="Who Are You?")

    async def on_submit(self, interaction: discord.Interaction):
        description = self.children[0].value
        queue_item = CharacterCreationQueueItem(
            interaction,description
        )
        config.character_creation_queue.put_nowait(queue_item)

        await interaction.response.send_message("Creating Character Please Wait~")


# Umu, I am so dead~
# Umu, I have to queue

async def getEquipmentText():
    # Grab data from json
    # Process Data
    # Display Data
    return "Here you go~"
