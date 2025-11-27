from pydantic import BaseModel
from typing_extensions import TypedDict


class WindowSize(TypedDict):
    width: int
    height: int


class GameWindow(BaseModel):
    caption: str
    size: WindowSize


class GameConfig(BaseModel):
    window: GameWindow


game_config = GameConfig(
    window=GameWindow(caption="Hot Rope", size=WindowSize(width=800, height=600))
)
