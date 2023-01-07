import datetime
import time
from datetime import datetime
from typing import List, Optional, Tuple

import discord
import pandas as pd


async def get_message_n(
    channel: discord.TextChannel,
    before: Optional[datetime] = None,
    after: Optional[datetime] = None,
    limit: Optional[int] = None,
    around: Optional[datetime] = None,
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


async def gather(
    channel: discord.TextChannel, days: Optional[int] = None
):  # Probably a better way to implement this
    """Gather message statistics for a given channel.

    Parameters
    ----------
    channel : discord.TextChannel
        The channel to gather message statistics from.

    days : int
        The amount of days to look back. (Gets passed to `channel.history()`)

    Returns
    -------
    pandas.DataFrame
        The gathered data.
    """
    raw_data = {}
    msg_data = await get_message_n(
        channel=channel,
        after=datetime.fromtimestamp(
            int(time.time()) - 86400 * days
        ),  # Get the timestamp from exactly n days ago
    )
    for msg in msg_data[1]:
        date_str = msg.created_at.strftime("%Y/%m/%d")
        if date_str in raw_data:
            raw_data[date_str] += 1
        else:
            raw_data[date_str] = 1
    fmt_data = {"date": [], "count": []}
    for (
        key,
        value,
    ) in raw_data.items():  # convert `raw_data` into a format pandas can understand
        fmt_data["date"].append(key)
        fmt_data["count"].append(value)

    dataframe = pd.DataFrame(data=fmt_data)
    return dataframe


async def gather_all(guild: discord.Guild, days: Optional[int] = None):
    """Same thing as `gather()` but for all channels in a guild.

    Parameters
    ----------
    guild : discord.TextChannel
        The guild to gather message statistics from.

    days : int or None, defaults to None
        The amount of days to look back. (Gets passed to `channel.history()`)

    Returns
    -------
    pandas.DataFrame
        The gathered data.
    """
    raw_data = {}
    for channel in guild.text_channels:
        msg_data = await get_message_n(
            channel=channel,
            after=datetime.fromtimestamp(
                int(time.time()) - 86400 * days
            ),  # Get the timestamp from exactly n days ago
        )
        for msg in msg_data[1]:
            date_str = msg.created_at.strftime("%Y/%m/%d")
            if date_str in raw_data:
                raw_data[date_str] += 1
            else:
                raw_data[date_str] = 1
    fmt_data = {"date": [], "count": []}
    for (
        key,
        value,
    ) in raw_data.items():  # convert `raw_data` into a format pandas can understand
        fmt_data["date"].append(key)
        fmt_data["count"].append(value)

    dataframe = pd.DataFrame(data=fmt_data)
    return dataframe
