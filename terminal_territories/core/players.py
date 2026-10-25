from dataclasses import dataclass, replace
from enum import Enum


class Actions(Enum):
    MOVE = 0
    EXPAND = 1
    ATTACK = 2
    FORTIFY = 3


@dataclass(frozen=True)
class Player:
    id: int
    name: str
    letter: str
    x: int
    y: int
    action: Actions = Actions.MOVE


def up(player: Player) -> Player:
    if player.x > 0 and player.x <= 7:
        return replace(player, x=player.x - 1)
    return player


def down(player: Player) -> Player:
    if player.x >= 0 and player.x < 7:
        return replace(player, x=player.x + 1)
    return player


def left(player: Player) -> Player:
    if player.y > 0 and player.y <= 11:
        return replace(player, y=player.y - 1)
    return player


def right(player: Player) -> Player:
    if player.y >= 0 and player.y < 11:
        return replace(player, y=player.y + 1)
    return player


def set_action(player: Player, action: Actions) -> Player:
    return replace(player, action=action)
