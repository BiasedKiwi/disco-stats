"""A collection of monitoring events (ex: on_ready, on_connect, etc...)"""
import logging
import os

import asyncpg
from discord.ext import commands
from dotenv import load_dotenv
from rich.console import Console

from .. import config  # pylint: disable=relative-beyond-top-level

load_dotenv()
console = Console()


class Monitors(commands.Cog):
    """Monitoring events."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = None  # pylint: disable=invalid-name
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        raw_config = config.get_raw_config()["postgresql"]
        params = {
            "user": os.environ.get("POSTGRES_USER"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
            "database": raw_config["postgres_db"],
            "host": raw_config["postgres_host"],
            "port": raw_config["postgres_port"],
        }
        self.db = await asyncpg.create_pool(**params)
        self.logger.info(
            "%s successfully connected to Postgres database at %s:%s with db '%s'",
            __name__,
            raw_config["postgres_host"],
            raw_config["postgres_port"],
            raw_config["postgres_db"],
        )
        self.logger.info("%s module loaded", __name__)

    @commands.Cog.listener()
    async def on_connect(self):
        """Called when the client connects to Discord. Not the same as on_ready"""
        self.logger.info("%s has successfully connected to Discord.", self.bot.user)

    @commands.Cog.listener()
    async def on_disconnect(self):
        """Called when the client has disconnected from Discord"""
        self.logger.warning(
            "%s has disconnected from Discord. This may not be important.",
            self.bot.user,
        )

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the client is done preparing the data received from Discord."""
        console.rule("[green bold]READY", characters="=")
        self.logger.info("%s is \u001b[32mready\u001b[0m for use.", self.bot.user)

    @commands.Cog.listener()
    async def on_socket_event_type(self, event_type):
        """Called whenever a websocket event is received from the WebSocket."""
        self.logger.debug("Got WebSocket event: %s", event_type)

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        """Called whenever a message is completely received from the WebSocket"""
        self.logger.debug("Got WebSocket message: %s", msg)

    @commands.Cog.listener()
    async def on_socket_raw_send(self, payload):
        """Called when the client has successfully connected to Discord."""
        self.logger.debug("Send operation done with payload: %s", payload)


async def setup(bot: commands.Bot):  # pylint: disable=missing-function-docstring
    await bot.add_cog(Monitors(bot))
