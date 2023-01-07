# pylint: disable=unused-import,missing-function-docstring,line-too-long
import logging

import discord
from discord import app_commands
from discord.ext import commands


class Misc(commands.Cog):
    """Miscellaneous commands"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        self.logger.info("%s module loaded", __name__)

    @app_commands.command(name="credits")
    async def credits(self, interaction: discord.Interaction):
        embed = discord.Embed(title="<:iconsshine:1061240486481899651> Credits")
        embed.add_field(
            name="<:iconslogo:1061239220200546355> Icons",
            value="Disco Stats uses icons made by **Creative Desire** ||https://discord.gg/aPvvhefmt3||",
        )
        embed.add_field(name="<:iconshammer:1061239727782633542> Creator", value="Made by hentyhentys#0001", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
