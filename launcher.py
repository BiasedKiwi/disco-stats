#!/usr/bin/env python
# pylint: disable=missing-function-docstring
"""Launcher script for Disco Stats the Discord bot.
"""

import logging
import os
from datetime import datetime

import asyncpg
import discord
from dotenv import load_dotenv
from rich.console import Console
from rich.traceback import install

import disco_stats
from disco_stats import Bot

install(show_locals=True, suppress=[discord, asyncpg])
console = Console()
console.rule("[yellow bold]LOADING", characters="=")

now = datetime.now()

logger = logging.getLogger("discord")  # Set up logging for discord
raw_conf = disco_stats.config.get_raw_config()

handler = logging.FileHandler(
    filename=f"./logs/{now.strftime('%Y-%m-%d_%H-%M-%S')}.log",
    encoding="utf-8",
    mode="w",
)
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(module)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

if raw_conf["logging"][0]["debug_logs"]:
    log_level = logging.DEBUG
    debug_events = True
    logger.warning(
        "Debug logging is turned on. For less verbose logging, set the 'debug_logs' key in /disco_stats/config/config.yaml to false."
    )
else:
    log_level = logging.INFO
    debug_events = False
    logger.warning(
        "Debug logging is turned off. For more verbose logging, set the 'debug_logs' key in /disco_stats/config/config.yaml to true"
    )
logger.setLevel(log_level)


# Constants
TOKEN = ""
PREFIX = ""

load_dotenv()  # Load the .env file
token = os.environ.get("DISCO_TOKEN")
if token is None:  # If the token was not found in the .env file, exit the program
    print(
        "Please provide a valid Discord API token. You can set an environment variable 'DISCO_TOKEN' to allow Disco Stats to access the token."
    )
    while (
        True
    ):  # If the program was executed from a binary, keep the terminal window alive.
        pass

TOKEN = token

if not raw_conf["debug"]["load_debug_cogs"]:
    ignored_cogs = raw_conf["debug"]["debug_cogs"]
else:
    ignored_cogs = []
intents = discord.Intents.default()


def set_intents():
    # pylint: disable=assigning-non-slot
    intents.message_content = True
    intents.guilds = True
    intents.members = True
    intents.voice_states = True


instance = Bot(
    command_prefix="..",
    intents=set_intents(),
    strip_after_prefix=True,
    case_insensitive=True,
    enable_debug_events=debug_events,
    ignore_cogs=ignored_cogs,
)  # Initialise a bot instance

logger.info("Welcome to Disco Stats")
try:
    instance.run(TOKEN, log_level=log_level)
except KeyboardInterrupt:
    logger.info("")
