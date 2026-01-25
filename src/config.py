from pydantic import BaseModel
from typing_extensions import TypedDict


class WindowSize(TypedDict):
    width: int
    height: int


class GameWindow(BaseModel):
    caption: str
    size: WindowSize


class Player(BaseModel):
    width: int
    height: int


class StarValues(BaseModel):
    one: int
    two: int
    three: int


class GameConfig(BaseModel):
    window: GameWindow
    player: Player
    star_values: StarValues


game_config = GameConfig(
    window=GameWindow(caption="Hot Rope", size=WindowSize(width=800, height=600)),
    player=Player(width=50, height=50),
    star_values=StarValues(one=50, two=100, three=150),
)
