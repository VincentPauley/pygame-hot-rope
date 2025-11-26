# from pydantic import BaseModel


# class WindowCaption(BaseModel):
#     caption: str

# class WindowSize(BaseModel):
#     width: int
#     height: int

# class GameConfig(BaseModel):
#     window: {
#         WindowCaption,

#     }

config = {
    "window": {"caption": "Hot Rope", "size": {"width": 800, "height": 600}},
}
