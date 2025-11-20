from typing import Tuple

from .rectangle import Rectangle, RectangleParams

# - should have methods to update position (requires frame delta)
# - should store it's own velocity vector
# - should store it's own speed


class MoveableRectangleParams(RectangleParams):
    velocity: Tuple[float, float] = (0.0, 0.0)  # (vx, vy)
    # speed: float = 0.0  # scalar speeed


# start with instantiating a rectangle with the correct entity type
class MoveableRectangle(Rectangle):
    def __init__(self, movable_rectangle_params: MoveableRectangleParams):
        movable_rectangle_params.entity_type = "moveable_rectangle"
        super().__init__(movable_rectangle_params)

        self.x_velocity = movable_rectangle_params.velocity[0]
        self.y_velocity = movable_rectangle_params.velocity[1]

    def reverse_x_velo(self):
        self.x_velocity = self.x_velocity * -1

    def reverse_y_velo(self):
        self.y_velocity = self.y_velocity * -1

    def update_pos(self, fame_delta: float):
        self.rect.x += self.x_velocity * fame_delta
        self.rect.y += self.y_velocity * fame_delta
