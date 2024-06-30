from discord import app_commands
import discord

# This is it baby wooooo~
def setup_alchemy_commands(tree: app_commands.CommandTree):
    
    @tree.command(name="alchemy_help", description="Show Alchemy Tutorial!")
    async def alchemy_help(interaction: discord.Interaction):
        
        await interaction.response.send_message(f"Alchemy Help Triggered!",ephemeral=True)
    
    @tree.command(name="alchemy_fusion", description="Combine Material!")
    async def alchemy_fusion(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"Alchemy Fusion Triggered!",ephemeral=True)

    @tree.command(name="alchemy_summon", description="Create Summon From Material!")
    async def alchemy_summon(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"Alchemy Summon Triggered!",ephemeral=True)

    
    @tree.command(name="alchemy_refine", description="Refine Equipment With Material!")
    async def alchemy_refine(interaction: discord.Interaction, name: str):
        
        await interaction.response.send_message(f"Alchemy Refine Triggered!",ephemeral=True)
