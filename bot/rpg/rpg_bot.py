import discord
from discord import app_commands

def setup_rpg_commands(tree: app_commands.CommandTree):
    
    @tree.command(name="rpg_stat", description="Show your current status!")
    async def rpg_stat(interaction: discord.Interaction):
        
        await interaction.response.send_message(f"RPG Status Triggered!", ephemeral=True)
    
    @tree.command(name="rpg_equipment", description="Show your current Equipment!")
    async def rpg_equipment(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"RPG Equipment Triggered!", ephemeral=True)

    @tree.command(name="rpg_player", description="Show your current Persona!")
    async def rpg_player(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"RPG Player Triggered!", ephemeral=True)

    @tree.command(name="rpg_item", description="Show your current materialss!")
    async def rpg_item(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"RPG Item Triggered!", ephemeral=True)