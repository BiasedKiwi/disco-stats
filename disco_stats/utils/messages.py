import datetime
from typing import List, Optional, Tuple

import discord


async def get_message_n(
    channel: discord.TextChannel,
    before: Optional[datetime.datetime] = None,
    after: Optional[datetime.datetime] = None,
    limit: Optional[int] = None,
    around: Optional[datetime.datetime] = None,
) -> Tuple[int, List[discord.Message]]:
    """Get the number of messages in a channel with the given filters.

    Parameters
    ----------
    channel : discord.TextChannel
        The text channel to get the messages from.
    before : Optional[datetime.datetime], optional
        Date to get messages before, by default None
    after : Optional[datetime.datetime], optional
        Date to get messages after, by default None
    limit : Optional[int], optional
        Message limit (newest first), by default None
    around : Optional[datetime.datetime], optional
        Date to get messages around, by default None

    Returns
    -------
    Tuple[int, List[discord.Message]]
        The number of messages and the list of messages.
    """
    messages = [
        message
        async for message in channel.history(
            before=before, after=after, limit=limit, around=around
        )
    ]
    return (len(messages), messages)
