# pylint: disable=unused-import,missing-function-docstring,relative-beyond-top-level,fixme
import logging

import discord
import pandas as pd
from discord import app_commands
from discord.ext import commands, tasks

from ..utils import messages


class MessageEvents(commands.Cog):
    """Message Events"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.get_bulk_msg_stats.start()  # pylint: disable=no-member

    async def cog_load(self):
        self.logger.info("%s module loaded", __name__)

    @tasks.loop(seconds=30)
    async def get_bulk_msg_stats(self):
        all_dataframes = {}
        for guild in self.bot.guilds:
            all_dataframes[guild.id] = await messages.gather_all(guild, 365)
        all_dataframes[883413709031108608].to_csv()  # TODO: Do something with this data

    @get_bulk_msg_stats.before_loop
    async def before_get_bulk_msg_stats(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(MessageEvents(bot))
