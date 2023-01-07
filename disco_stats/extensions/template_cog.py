# pylint: disable=unused-import,missing-function-docstring
import logging

import discord
from discord import app_commands
from discord.ext import commands


class TemplateCog(commands.Cog):
    """basically a template cog"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        self.logger.info("%s module loaded", __name__)


async def setup(bot):
    await bot.add_cog(TemplateCog(bot))
