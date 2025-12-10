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

class GameConfig(BaseModel):
    window: GameWindow
    player: Player


game_config = GameConfig(
    window=GameWindow(caption="Hot Rope", size=WindowSize(width=800, height=600)),
    player=Player(width=50, height=50)
)
