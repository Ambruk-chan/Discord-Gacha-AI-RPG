import re

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


async def get_thread_history(thread:discord.Thread, append=None, n=20):
    history = []
    if append:
        history.append(append)
    async for message in thread.history(limit=n):
        name = str(message.author.display_name)

        # Sanitize the name by removing spaces, special characters, and converting to lowercase
        sanitized_name = re.sub(r'[^\w]', '', name)

        content = re.sub(r'<@!?[0-9]+>', '', message.content)  # Remove user mentions
        if content.startswith("[System"):
            history.append(content.strip())
        else:
            history.append(f"[Reply] {sanitized_name}: {content.strip()}")

    # Reverse the order of the collected messages
    history.reverse()
    contents = "\n\n".join(history)
    return contents
