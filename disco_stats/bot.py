#!/usr/bin/env python
import sys
from pkgutil import iter_modules
from typing import List, Optional

try:
    from discord.ext import commands
    from rich.console import Console
except ImportError:
    print(
        "Missing required libraries, please install them. (pip install -r requirements.txt)"
    )
    sys.exit(1)


console = Console()


class Bot(commands.AutoShardedBot):
    """Main bot constructor."""

    def __init__(self, **kwargs):
        self.case_insensitive = True
        self.strip_after_prefix = True
        self.ignore_cogs = kwargs["ignore_cogs"]
        super().__init__(**kwargs)

    async def setup_hook(self):
        # Code here run after the bot has logged in, but before it has connected to the Websocket.
        await self.load_cogs(client_obj=self, ignore=self.ignore_cogs)

    @staticmethod
    async def load_cogs(
        client_obj: commands.AutoShardedBot, ignore: Optional[List] = None
    ) -> None:
        """Iterate through all cogs in a directory using `pkgutil.iter_modules` and load them.


        Parameters
        ----------
        client_obj : commands.AutoShardedBot
            The bot instance to load cogs into.

        ignore : list, optional
            List of module names to ignore, by default []
        """
        all_extensions = [
            m.name
            for m in iter_modules(
                ["./disco_stats/extensions"], prefix="disco_stats.extensions."
            )
        ]
        if ignore is None:
            return
        for ext in all_extensions:
            if ext in ignore:
                continue
            await client_obj.load_extension(ext)


if __name__ == "__main__":
    print("Please launch the launcher.py file instead of this one directly.")
    sys.exit(1)
