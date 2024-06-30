import discord


async def send_webhook_message(channel: discord.abc.GuildChannel, content: str, avatar_url: str, username: str) -> None:
    # Check if the channel is a text channel or a thread
    if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.Thread):
        webhook_list = await channel.webhooks()

        for webhook in webhook_list:
            if webhook.name == "AktivaAI":
                await webhook.send(content, username=username, avatar_url=avatar_url)
                return

        webhook = await channel.create_webhook(name="AktivaAI")
        await webhook.send(content, username=username, avatar_url=avatar_url)
    else:
        print("The channel must be either a TextChannel or a Thread.")
    return
