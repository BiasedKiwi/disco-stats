# pylint: disable=protected-access,missing-function-docstring,missing-class-docstring,line-too-long
"""A collection of debug commands. These shouldn't be enabled in production environments.
They can be disabled by setting the 'debug_comands' key in /barnacle/config/config.yaml."""
import logging
from typing import Optional, Literal

import discord
from discord import app_commands
from discord.ext import commands


class DebugCmds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        self.logger.info("%s module loaded", __name__)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self, ctx, guilds=None, spec: Optional[Literal["~", "*", "^"]] = None
    ) -> None:
        """Credits: https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f"""
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @app_commands.command(name="reload", description="Debug only. Reload cogs")
    async def reload(self, interaction: discord.Interaction, cog: str):
        await self.bot.reload_extension(cog)
        await interaction.response.send_message(f"done reloading {cog}")

    @sync.error
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
