"""Message statistics."""
import logging

from discord.ext import commands


class MessageStats(commands.Cog):
    """Cog to gather message statistics."""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        self.logger.info("%s module loaded", __name__)


async def setup(bot):  # pylint: disable=missing-function-docstring
    await bot.add_cog(MessageStats(bot))
