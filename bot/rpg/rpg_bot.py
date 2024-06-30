import discord
from discord import app_commands
import rpg_engine

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
        self.add_item(discord.ui.TextInput(label="Weapon Description", placeholder="Just put it in"))
        self.add_item(discord.ui.TextInput(label="Armor Description", placeholder="Just put it in"))
        self.add_item(discord.ui.TextInput(label="Possession Description", placeholder="Just put it in"))
        self.add_item(discord.ui.TextInput(label="Power Description", placeholder="Just put it in"))
       
    async def on_submit(self, interaction: discord.Interaction):
        user_data = interaction.message.author
        description = self.children[0].value
        weapon = self.children[1].value
        armor = self.children[2].value
        possession = self.children[3].value
        power = self.children[4].value
        
        await rpg_engine.generate_new_player(user_data, description, weapon, armor, possession, power)

        await interaction.response.send_message("Starting Your Journey...")

#Umu, I am so dead~

async def getEquipmentText():
    # Grab data from json
    # Process Data
    # Display Data
    return "Here you go~"