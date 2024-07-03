from discord import app_commands
import discord


def setup_battle_commands(tree: app_commands.CommandTree):
    group = app_commands.Group(name="battle", description="Battle Commands!!!")

    @group.command(name="help", description="Show Battle Tutorial!")
    async def battle_help(interaction: discord.Interaction):
        await interaction.response.send_message(f"Battle Help Triggered!",ephemeral=True)

    @group.command(name="action", description="Do An Action!")
    async def battle_action(interaction: discord.Interaction):
        await interaction.response.send_message(f"Battle Action Triggered!",ephemeral=True)

    @group.command(name="check", description="Check Your Stats and Other Useful Stuff In Battle!!")
    async def battle_check(interaction: discord.Interaction):
        await interaction.response.send_message(f"Battle Check Triggered!",ephemeral=True)


    @group.command(name="use", description="Check Your Stats and Other Useful Stuff In Battle!!")
    async def battle_use(interaction: discord.Interaction):
        await interaction.response.send_message(f"Battle Use Item Triggered!",ephemeral=True)

    @group.command(name="flee", description="Run from the current battle!")
    async def battle_flee(interaction: discord.Interaction):
        await interaction.response.send_message(f"Battle Flee Triggered!",ephemeral=True)
    tree.add_command(group)

