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
        self.velocity = movable_rectangle_params.velocity

    def update_pos(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    # coords is already on the Rectangle via rect.x & rect.y, might be
    # bett

    #     self.velocity = velocity  # (vx, vy)
    #     self.speed = speed  # scalar speed

    # def update_position(self, delta_time):
    #     self.x += self.velocity[0] * self.speed * delta_time
    #     self.y += self.velocity[1] * self.speed * delta_time
