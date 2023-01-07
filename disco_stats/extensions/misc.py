# pylint: disable=unused-import,missing-function-docstring,line-too-long,no-member
import logging
import random

import discord
from discord.ext import tasks
from discord import app_commands
from discord.ext import commands


class Misc(commands.Cog):
    """Miscellaneous commands"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.change_presence.start()

    async def cog_load(self):
        self.logger.info("%s module loaded", __name__)

    @app_commands.command(name="credits")
    async def credits(self, interaction: discord.Interaction):
        embed = discord.Embed(title="<:iconsshine:1061240486481899651> Credits")
        embed.add_field(
            name="<:iconslogo:1061239220200546355> Icons",
            value="Disco Stats uses icons made by **Creative Desire** ||https://discord.gg/aPvvhefmt3||",
        )
        embed.add_field(
            name="<:iconshammer:1061239727782633542> Creator",
            value="Made by hentyhentys#0001",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @tasks.loop(minutes=5)
    async def change_presence(self):
        all_presence = [
            discord.Game(name="Counting messages..."),
            discord.Activity(
                type=discord.ActivityType.watching, name="Server stats..."
            ),
        ]
        await self.bot.change_presence(activity=random.choice(all_presence))

    @change_presence.before_loop
    async def before_change_presence(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Misc(bot))
