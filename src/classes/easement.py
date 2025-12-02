# Note: this is a very crude implementation of an easement that moves between two points
class Easement:
    def __init__(self, point_a, point_b, velo=1):
        if point_a > point_b:
            raise ValueError("point_a must be less than point_b")

        self.point_a = point_a
        self.point_b = point_b
        self.velocity = velo
        self.original_velocity = velo

        self.current_position = point_a

        self.midpoint = (point_a + point_b) / 2

        self.moving_toward_b = True
        self.moving_toward_a = False

    def describe(self):
        print(f"Easement POS {self.current_position}")

    def update(self, delta):
        if self.moving_toward_b:
            self.current_position += self.velocity * delta * 60

            if self.current_position > self.midpoint:
                self.velocity -= 0.05  # this is likely to decrease past the point where it can come back
            else:
                # first block is hitting this
                self.velocity += 0.05  # it's going to increase toward the midpoint

            # check for the end and reversal
            if self.current_position >= self.point_b:
                self.current_position = self.point_b
                self.moving_toward_b = False
                self.moving_toward_a = True
                self.velocity = self.original_velocity * -1
        elif self.moving_toward_a:
            self.current_position += self.velocity * delta * 60

            if self.current_position > self.midpoint:
                self.velocity -= 0.05
            else:
                self.velocity += 0.05
            # check for the end and reversal
            if self.current_position <= self.point_a:
                self.current_position = self.point_a
                self.moving_toward_a = False
                self.moving_toward_b = True
                self.velocity = self.original_velocity
