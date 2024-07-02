from typing import Any

import discord
from discord.types.snowflake import Snowflake


async def send_webhook_message(channel: discord.abc.GuildChannel | discord.Thread, content: str, avatar_url: str = "https://i.imgur.com/rpd75Pr.jpg", username: str = "RPG") -> None:
    # Store thread id for later, if channel is a thread
    thread: Snowflake | None = None
    if isinstance(channel, discord.Thread):
        parent = channel.parent
        if parent is None:
            return
        thread = channel.id
        channel = parent

    if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.ForumChannel):
        # Try to find the right webhook
        webhook_list = await channel.webhooks()
        kwargs: dict[str, Any] = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url,
        }
        if thread:  # try to send webhook message in thread
            kwargs["thread"] = thread

        for webhook in webhook_list:
            if webhook.name == "RPGAI":
                await webhook.send(**kwargs)
                return
        webhook = await channel.create_webhook(name="RPGAI")
        await webhook.send(**kwargs)
    else:
        print("The channel must be either a TextChannel or a Thread.")
    return
