from .rectangle import Rectangle, RectangleParams

# - should base itself from rectangle but be sure to overwrite the entity type.
# - should have methods to update position (requires frame delta)
# - should store it's own velocity vector
# - should store it's own speed


# start with instantiating a rectangle with the correct entity type
class MoveableRectangle(Rectangle):
    def __init__(self, movable_rectangle_params: RectangleParams):
        # entity_type should be hard-set from within here, combined with
        movable_rectangle_params.entity_type = "moveable_rectangle"

        super().__init__(movable_rectangle_params)

    # def __init__(self, rectangle_params: RectangleParams, velocity=(0, 0), speed=0):
    #     super().__init__(rectangle_params)
    #     self.entity_type = "movable_rectangle"  # overwrite entity type
    #     self.velocity = velocity  # (vx, vy)
    #     self.speed = speed  # scalar speed

    # def update_position(self, delta_time):
    #     self.x += self.velocity[0] * self.speed * delta_time
    #     self.y += self.velocity[1] * self.speed * delta_time
