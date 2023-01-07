#!/usr/bin/env python
# pylint: disable=missing-function-docstring,invalid-name,line-too-long
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

# Setup rich console
install(show_locals=True, suppress=[discord, asyncpg])
console = Console()
console.rule("[yellow bold]LOADING", characters="=")

raw_conf = disco_stats.config.get_raw_config()
now = datetime.now()


def setup_logger():
    logger = logging.getLogger("discord")

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
    return (logger, debug_events, log_level)


def get_token():
    load_dotenv()  # Load the .env file
    token = os.environ.get("DISCO_TOKEN")
    if token is None:
        print(
            "Please provide a valid Discord API token. You can set an environment variable 'DISCO_TOKEN' to allow Disco Stats to access the token."
        )
        while (
            True
        ):  # If the program was executed from a binary, keep the terminal window alive.
            pass

    return token


def get_ignored_cogs():
    if not raw_conf["debug"]["load_debug_cogs"]:
        return raw_conf["debug"]["debug_cogs"]
    return []


intents = discord.Intents.default()


def set_intents():
    # pylint: disable=assigning-non-slot
    intents.message_content = True
    intents.guilds = True
    intents.members = True
    intents.voice_states = True
    return intents

if __name__ == "__main__":
    _logger = setup_logger()

    instance = Bot(
        command_prefix="?",
        intents=set_intents(),
        strip_after_prefix=True,
        case_insensitive=True,
        enable_debug_events=_logger[1],
        ignore_cogs=get_ignored_cogs(),
    )  # Initialise a bot instance

    _logger[0].info("Welcome to Disco Stats")
    try:
        instance.run(get_token(), log_level=_logger[2])
    except KeyboardInterrupt:
        _logger[0].info("")
