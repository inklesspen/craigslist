from discord.ext import commands
import discord
from typing import Dict
from .model import GameState, NoCurrentDrawError, UnfinishedDrawError

bot = commands.Bot(command_prefix="~")
game_registry: Dict[discord.Guild, GameState] = {}


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
async def begin(ctx: commands.Context) -> None:
    if ctx.guild is None:
        await ctx.send(f"{ctx.command} can only be used inside a server.")
        return
    if ctx.guild in game_registry:
        await ctx.send("A game is already running. End it first.")
        return
    realtor: discord.abc.User = ctx.message.author
    game_registry[ctx.guild] = GameState(realtor=realtor)
    await ctx.send(f"A new game has begun. {realtor.mention} is the realtor.")


@bot.command()
async def draw(ctx: commands.Context) -> None:
    if ctx.guild is None:
        await ctx.send(f"{ctx.command} can only be used inside a server.")
        return
    if ctx.guild not in game_registry:
        await ctx.send("No game is being played.")
        return
    state: GameState = game_registry[ctx.guild]
    try:
        state.draw()
    except UnfinishedDrawError:
        await ctx.send(
            "The current draw has not fully been revealed. To draw anyway, run this command again."
        )
        return
    current_draw_string = state.describe_current_draw()
    await state.realtor.send(current_draw_string)
    await ctx.send(f"{len(state.current_draw)} beads have been drawn.")


@bot.command()
async def reveal(ctx: commands.Context) -> None:
    if ctx.guild is None:
        await ctx.send(f"{ctx.command} can only be used inside a server.")
        return
    if ctx.guild not in game_registry:
        await ctx.send("No game is being played.")
        return
    state: GameState = game_registry[ctx.guild]
    try:
        color = state.reveal()
    except NoCurrentDrawError:
        await ctx.send("There are no beads remaining to be revealed.")
        return
    if state.current_draw is None:
        concluded = "draw"
        if state.completed_draw_count == 3:
            del game_registry[ctx.guild]
            concluded = "game"
        await ctx.send(f"The next bead is {color}. This concludes the current {concluded}.")
        return
    await ctx.send(
        f"The next bead is {color}. {len(state.current_draw)} beads remain to be revealed."
    )


@bot.command()
async def end(ctx: commands.Context) -> None:
    if ctx.guild is None:
        await ctx.send(f"{ctx.command} can only be used inside a server.")
        return
    if ctx.guild not in game_registry:
        await ctx.send("No game is being played.")
        return
    del game_registry[ctx.guild]
    await ctx.send("The game has been ended.")
