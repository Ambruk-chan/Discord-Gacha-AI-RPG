import discord


async def send_webhook_message(channel: discord.abc.GuildChannel, content: str, avatar_url: str = "https://i.imgur.com/rpd75Pr.jpg", username: str = "RPG") -> None:
    # Check if the channel is a text channel or a thread
    if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.Thread):
        webhook_list = await channel.webhooks()

        webhook = None
        for existing_webhook in webhook_list:
            if existing_webhook.name == "RPGAI":
                webhook = existing_webhook
                break

        if not webhook:
            webhook = await channel.create_webhook(name="RPGAI")

        # Split content into chunks of 2000 characters or less
        chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]

        for chunk in chunks:
            await webhook.send(chunk, username=username, avatar_url=avatar_url)
    else:
        print("The channel must be either a TextChannel or a Thread.")
    return
