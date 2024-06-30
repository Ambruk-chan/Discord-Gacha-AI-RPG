from discord import app_commands
import discord

def setup_dungeon_commands(tree: app_commands.CommandTree):
    
    @tree.command(name="dungeon_help", description="Show Battle Tutorial!")
    async def dungeon_help(interaction: discord.Interaction):
        
        await interaction.response.send_message(f"Battle Help Triggered!",ephemeral=True)

    @tree.command(name="dungeon_create", description="Do An Action!")
    async def dungeon_create(interaction: discord.Interaction):
        
        await interaction.response.send_message(f"Battle Action Triggered!",ephemeral=True)

    @tree.command(name="dungeon_choice", description="Check Your Stats and Other Useful Stuff In Battle!!")
    async def dungeon_choice(interaction: discord.Interaction):
        
        await interaction.response.send_message(f"Battle Check Triggered!",ephemeral=True)

    @tree.command(name="dungeon_abandon", description="Abandon The Dungeon (WILL DESTROY THE DUNGEON)")
    async def dungeon_abandon(interaction: discord.Interaction):
        
        await interaction.response.send_message(f"Dungeon Destroyed and Abandoned!!!",ephemeral=True)
    
    
   