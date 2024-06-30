import random
import logging
from typing import Optional
import uuid
from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, Interaction, InteractionType
from discord.ui import View, Button, Select
from discord import ButtonStyle, SelectOption, app_commands
from discord.app_commands import Choice


logger = logging.getLogger(__name__)


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.embeds = Embeds(bot)
        self.views = Views(bot)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f"Cog {self.__class__.__name__} loaded")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction) -> None:
        if interaction.type == InteractionType.component:
            await self.on_button_click(interaction)

    async def on_button_click(self, interaction: Interaction) -> None:
        if interaction.data['custom_id'] == "cog_list":
            await interaction.response.edit_message(embed=self.embeds.cog_list,
                                                    view=self.views.cog_list(await self.bot.is_owner(interaction.user)))
        elif interaction.data['custom_id'] == "info":
            await interaction.response.edit_message(embed=self.embeds.info, view=self.views.info)
        elif interaction.data['custom_id'] == "reload_cog":
            if not await self.bot.is_owner(interaction.user):
                await interaction.response.edit_message(content=":x: You have no permission to do this.", view=None,
                                                        embed=None)
            await self.bot.reload_extension(f'cogs.{interaction.data["values"][0]}')
            await interaction.response.edit_message(content=":white_check_mark: Done.", view=None, embed=None)
        elif interaction.data['custom_id'] == "reload_cog_menu":
            view = self.views.reload_cog
            view.add_item(
                Button(label="Cancel", custom_id="cog_list", style=ButtonStyle.red))
            await interaction.response.edit_message(view=view)
        elif interaction.data['custom_id'] == "uuid_regenerate":
            await interaction.response.edit_message(content=f"The uuid is: `{str(uuid.uuid4())}`",
                                                    view=self.views.uuid)

    async def cog_auto_complete(self, interaction: Interaction, current: str):
        return [Choice(name=cog, value=cog) for cog in self.bot.cogs if current.lower() in cog.lower()]

    @commands.hybrid_command(name="reload", description="Reload a cog")
    @commands.is_owner()
    @app_commands.autocomplete(cog=cog_auto_complete)
    @app_commands.describe(cog="The cog name to reload")
    async def reload(self, ctx: Context, cog: Optional[str] = None) -> None:
        if cog is None:
            await ctx.send("Please select a cog from following list", view=self.views.reload_cog,
                           ephemeral=True)
            return
        if cog not in [str(cog) for cog in self.bot.cogs]:
            await ctx.send("Cog not found, please select a cog from following list",
                           view=self.views.reload_cog, ephemeral=True)
            return
        try:
            await self.bot.reload_extension(f'cogs.{cog.lower()}')
            await ctx.send(content=":white_check_mark: Done.", view=None, embed=None, ephemeral=True)

        except Exception as e:
            await ctx.send(f":x: {e}", ephemeral=True)

    @commands.hybrid_command(name="ping", description="Get the latency of bot")
    async def ping(self, ctx: Context) -> None:
        embed = Embed(
            title="Pong!", description=f"Latency is: {round(self.bot.latency * 1000)}ms", color=0x1ee3b8)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="info", description="Get bot info")
    async def info(self, ctx):
        await ctx.send(embed=self.embeds.info, view=self.views.info, ephemeral=True)

    @commands.hybrid_command(name="cog_list", description="Get cog list")
    async def list_cog(self, ctx):
        await ctx.send(embed=self.embeds.cog_list, view=self.views.cog_list(), ephemeral=True)

    @commands.hybrid_command(name="random", description="Get a random number")
    @app_commands.describe(minimum="The minimum number", maximum="The maximum number")
    async def random(self, ctx, minimum: int = 1, maximum: int = 6, private: bool = True):
        await ctx.send(f"Random number: `{random.randint(minimum, maximum)}`", ephemeral=private)

    @commands.hybrid_command(name="uuid", description="Get a random uuid")
    @app_commands.describe(with_hyphens="Whether to include hyphens in the uuid")
    async def uuid(self, ctx, with_hyphens: bool = True, private: bool = True):
        await ctx.send(f"The uuid is: `{str(uuid.uuid4()) if with_hyphens else uuid.uuid4().hex}`",
                       view=self.views.uuid, ephemeral=private)

    @commands.hybrid_command(name="delete", description="Delete a message")
    @app_commands.describe(limit="The number of messages to delete (default 1)")
    async def delete(self, ctx, limit: int = 1):
        await ctx.channel.purge(limit=limit + 1)


class Embeds:
    def __init__(self, bot):
        self.bot = bot

    @property
    def info(self):
        embed = Embed(title=":information: Bot info", color=0x1ee3b8)
        embed.add_field(name="Name", value="Bot", inline=False)
        embed.add_field(
            name="Version", value=":construction: Work in progress", inline=False)
        embed.add_field(name="Developer", value="caru-ini", inline=False)
        embed.set_footer(text="❤️Made with discord.py")
        return embed

    @property
    def cog_list(self):
        embed = Embed(title=":gear: Cog List", color=0x1ee3b8)
        for cog in self.bot.cogs:
            embed.add_field(
                name=cog, value=self.bot.cogs[cog].description, inline=False)
        return embed


class Views:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def cog_list(reload=False):
        view = View()
        view.add_item(Button(label="Information", custom_id="info",
                      style=ButtonStyle.green, emoji="ℹ️"))
        if reload:
            view.add_item(Button(
                label="Reload", custom_id="reload_cog_menu", style=ButtonStyle.green, emoji="🔄"))
        return view

    @property
    def info(self):
        view = View()
        view.add_item(Button(label="Cog List", custom_id="cog_list",
                      style=ButtonStyle.green, emoji="📜"))
        view.add_item(Button(
            label="GitHub", url="https://github.com/caru-ini/", style=ButtonStyle.link, emoji="🐈"))
        return view

    @property
    def reload_cog(self):
        view = View()
        view.add_item(Select(options=[SelectOption(label=cog, value=cog.lower()) for cog in self.bot.cogs],
                             placeholder="Select a cog to reload", custom_id="reload_cog"))
        return view

    @property
    def uuid(self):
        view = View()
        view.add_item(Button(emoji="🔄", custom_id="uuid_regenerate"))
        return view


async def setup(bot):
    await bot.add_cog(General(bot))
