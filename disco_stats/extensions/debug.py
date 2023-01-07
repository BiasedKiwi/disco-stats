# pylint: disable=protected-access,missing-function-docstring,missing-class-docstring
"""A collection of debug commands. These shouldn't be enabled in production environments.
They can be disabled by setting the 'debug_comands' key in /barnacle/config/config.yaml."""
import logging

import discord
from discord import app_commands
from discord.ext import commands


class DebugCmds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        self.logger.info("%s module loaded", __name__)

    @commands.command(name="sync")
    @commands.is_owner()
    async def _sync(self, ctx: commands.Context):
        await self.bot.tree.sync()
        embed = discord.Embed(
            title="Done!", description="Successfully synced all commands globally."
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author._avatar)
        await ctx.channel.send(embed=embed)

    @app_commands.command(name="reload", description="Debug only. Reload cogs")
    async def reload(self, interaction: discord.Interaction, cog: str):
        await self.bot.reload_extension(cog)
        await interaction.response.send_message(f"done reloading {cog}")

    @_sync.error
    @reload.error
    async def on_sync_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        """Called when `sync` fails"""
        if isinstance(error, commands.errors.NotOwner):
            self.logger.critical("Possibly forgot to disable debug commands.")
            await interaction.response.send_message(
                "Only the owner of the bot can execute this command!"
            )
        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(DebugCmds(bot))
