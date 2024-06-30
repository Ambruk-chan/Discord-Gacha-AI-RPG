from discord import app_commands
import discord

#The INITS
def setup_dungeon_commands(tree: app_commands.CommandTree):
    
    @tree.command(name="dungeon_help", description="Show Battle Tutorial!")
    async def dungeon_help(interaction: discord.Interaction):
        help = show_dungeon_help()
        await interaction.response.send_message(help,ephemeral=True)

    @tree.command(name="dungeon_create", description="Create a New Dungeon!")
    async def dungeon_create(interaction: discord.Interaction):
        result = dungeon_creation_check(interaction)
        await interaction.response.send_message(result,ephemeral=True)

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

