import dataclasses
from collections import Counter
from typing import List, Optional
import random
import discord.abc


@dataclasses.dataclass(order=True, frozen=True)
class BeadType:
    """Class representing a type of bead."""

    color: str = dataclasses.field(compare=False, hash=True)
    value: int = dataclasses.field(compare=True, hash=False)
    remove_from_pool: bool = dataclasses.field(default=True, compare=False, hash=True)

    def __str__(self) -> str:
        return self.color


GREEN_BEAD = BeadType(color="green", value=2)
RED_BEAD = BeadType(color="red", value=1)
BLACK_BEAD = BeadType(color="black", value=-1, remove_from_pool=False)


@dataclasses.dataclass
class GameState:
    """State of a MAH game."""

    pool: Counter = dataclasses.field(
        default_factory=lambda: Counter({GREEN_BEAD: 5, RED_BEAD: 8, BLACK_BEAD: 2})
    )
    current_draw: Optional[List[BeadType]] = dataclasses.field(default=None)
    realtor: Optional[discord.abc.User] = dataclasses.field(default=None)
    unfinished_draw_warning_given: bool = dataclasses.field(default=False)
    completed_draw_count: int = 0

    def describe_current_draw(self) -> str:
        if self.current_draw is None:
            raise NoCurrentDrawError()
        colors = ", ".join([str(b) for b in self.current_draw])
        value = sum([b.value for b in self.current_draw])
        return f"{colors} = {value}"

    def draw(self) -> None:
        if self.current_draw is not None and not self.unfinished_draw_warning_given:
            self.unfinished_draw_warning_given = True
            raise UnfinishedDrawError()
        self.current_draw = random.sample(list(self.pool.elements()), 5)
        to_remove = [b for b in self.current_draw if b.remove_from_pool]
        self.pool.subtract(to_remove)
        self.unfinished_draw_warning_given = False

    def reveal(self) -> str:
        if self.current_draw is None:
            raise NoCurrentDrawError()
        drawn = self.current_draw.pop(0)
        if len(self.current_draw) == 0:
            self.current_draw = None
            self.completed_draw_count += 1
        return str(drawn)


class NoCurrentDrawError(Exception):
    pass


class UnfinishedDrawError(Exception):
    pass
