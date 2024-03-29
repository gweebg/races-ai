from pydantic import BaseModel


class Coordinates(BaseModel):
    x: int
    y: int

    @classmethod
    def empty(cls) -> 'Coordinates':
        return cls(x=0, y=0)

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __eq__(self, other: 'Coordinates') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x * 0x1f1f1f1f) ^ self.y)


class RaceCar:
    """
    This class represents a car in the app.
    A car has its position, velocity and acceleration.
    """

    def __init__(self, pos=Coordinates.empty(), vel=Coordinates.empty(), acc=Coordinates.empty()):

        self.pos: Coordinates = pos
        self.vel: Coordinates = vel
        self.acc: Coordinates = acc

    def __eq__(self, other: 'RaceCar'):
        return (self.pos == other.pos) and (self.vel == other.vel)

    def update(self):
        """
        Updates the car velocity and position based on its acceleration.
        """

        self.vel.x += self.acc.x
        self.vel.y += self.acc.y

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def __str__(self):
        return f"pos:{self.pos}, vel:{self.vel}"

    def update_vel(self):
        """
        Only update the velocity of the car according to its current acceleration.
        """

        self.vel.x += self.acc.x
        self.vel.y += self.acc.y

    # The following methods represent every possible play made by the car.

    def accel_up(self):
        self.acc.y = -1
        self.update_vel()

    def accel_down(self):
        self.acc.y = 1
        self.update_vel()

    def accel_left(self):
        self.acc.x = -1
        self.update_vel()

    def accel_right(self):
        self.acc.x = 1
        self.update_vel()

    def accel_top_left(self):
        self.acc.x = -1
        self.acc.y = -1
        self.update_vel()

    def accel_top_right(self):
        self.acc.x = 1
        self.acc.y = -1
        self.update_vel()

    def accel_down_left(self):
        self.acc.x = -1
        self.acc.y = 1
        self.update_vel()

    def accel_down_right(self):
        self.acc.x = 1
        self.acc.y = 1
        self.update_vel()

    def set_acc_zero(self):
        self.acc.x = 0
        self.acc.y = 0

    def set_vel_zero(self):
        self.vel.x = 0
        self.vel.y = 0

    def __hash__(self):
        return hash(self.pos.x + self.pos.y + self.vel.x + self.vel.y)
