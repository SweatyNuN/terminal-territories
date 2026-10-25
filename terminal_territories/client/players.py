from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Player:
    id: int
    name: str
    letter: str
    x: int
    y: int


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
