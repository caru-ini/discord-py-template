import json
import os
import asyncio
import sys
from pathlib import Path
from typing import List, Literal, Optional
import discord

from discord.ext import commands
from discord import Intents

from dotenv import load_dotenv

from rich.logging import RichHandler
from rich.console import Console

import logging

load_dotenv()

CONFIG_PATH = Path(os.getenv("CONFIG_PATH", "config.json"))
LOG_PATH = Path(os.getenv("LOG_PATH", "bot.log"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
TOKEN = os.getenv("TOKEN")

console = Console()

logging.basicConfig(
    level=logging.getLevelName(LOG_LEVEL),
    handlers=[RichHandler(console=console, markup=True),
              logging.FileHandler(filename=LOG_PATH)],
    format="\[%(name)s] %(message)s",
    datefmt="[%X]",
)

logger = logging.getLogger("bot_main")


def load_config() -> None:
    config_path = Path(os.getenv("CONFIG_PATH", "config.json"))
    if not config_path.exists():
        Path(config_path).touch()
        Path(config_path).write_text(json.dumps({
            "prefix": "!",
            "invite": "<>",
        }))


async def scan_all_cogs() -> List[str]:
    """
    Scan all cogs in the cogs directory
    Package cogs also supported
    """
    cogs = []

    # get .py cogs
    for file in Path("cogs").glob("*.py"):
        if file.stem == "__init__":
            continue
        cogs.append(f"cogs.{file.stem}")

    # get package cogs
    for folder in Path("cogs").glob("*"):
        if folder.is_dir():
            # check if folder is a package
            if (folder / "__init__.py").exists():
                cogs.append(f"cogs.{folder.name}")
                continue
            # exclude __pycache__
            if (folder / "__pycache__").exists():
                continue

            logger.warning(f"Folder {folder} is not a valid cog package")

    logger.info(f"Scanned cogs: {cogs}")
    return cogs

bot = commands.Bot(command_prefix='!', intents=Intents.all())

bot.owner_ids = [int(id) for id in os.getenv('OWNERS', '').split(',')]


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")
    active_guilds = len(bot.guilds)
    if not active_guilds:
        invite_link = discord.utils.oauth_url(
            bot.user.id, permissions=discord.Permissions(permissions=8))
        logger.warning(
            f"Bot seems to be in no guilds. Access link to invite. \nInvite link: {invite_link}")
    logger.info(f"Active in {active_guilds} guilds")


# Umbra's Sync Command
# Source: https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    async with ctx.typing():
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


async def main() -> None:
    async def load_cogs():
        loaded = []
        error = []

        for cog in (await scan_all_cogs()):
            try:
                await bot.load_extension(cog)
                loaded.append(cog)
            except commands.ExtensionError as e:
                logger.exception(f'Failed to load extension \"{cog}\"\n{e}')
                error.append(cog)

        logger.info(
            f"[green]Loaded [/green]: {len(loaded)} cogs: \n{loaded}") if loaded else None
        logger.info(
            f"[red]Error [/red]: {len(error)} cogs: \n{error}") if error else None
        if not loaded:
            logger.error("No cogs loaded. Exiting.")
            sys.exit(1)

    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("Bye!")
