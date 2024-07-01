import asyncio
import discord
from discord import app_commands
import config

def setup_rpg_commands(tree: app_commands.CommandTree):

    @tree.command(name="rpg_begin", description="Begin Your Story!!!")
    async def rpg_stat(interaction: discord.Interaction):
        # Pull up character creation modal
        await interaction.response.send_modal(CharacterCreatorModal())
    
    @tree.command(name="rpg_equipment", description="Show your current Equipment!")
    async def rpg_equipment(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"RPG Equipment Triggered!", ephemeral=True)

    @tree.command(name="rpg_player", description="Show your current Persona!")
    async def rpg_player(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"RPG Player Triggered!", ephemeral=True)

    @tree.command(name="rpg_item", description="Show your current materialss!")
    async def rpg_item(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"RPG Item Triggered!", ephemeral=True)


class CharacterCreatorModal(discord.ui.Modal, title='Create Character'):
    def __init__(self):
        super().__init__()
        
        self.add_item(discord.ui.TextInput(label="About Yourself", placeholder="Who Are You?"))
       
    async def on_submit(self, interaction: discord.Interaction):
        description = self.children[0].value
        queue_item = {
        "interaction_data" : interaction,
        "description" : description
        }
        config.process_player_request.put_nowait(queue_item)
        await interaction.response.send_message("Creating Character Please Wait~")
        

        

# Umu, I am so dead~
# Umu, I have to queue

async def getEquipmentText():
    # Grab data from json
    # Process Data
    # Display Data
    return "Here you go~"