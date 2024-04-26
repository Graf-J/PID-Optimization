from math import sin, cos, radians, degrees
from typing import Tuple


class Simulation:
    ROLLING_FRICTION_COEFFICIENT = 0.05
    GRAVITY_CONSTANT = 9.81

    def __init__(
            self,
            mass: float,
            delta_t: float,
            initial_angle: float = 0.0,
            initial_velocity_x: float = 0.0,
            initial_position_x: float = 0.0):
        self.mass = mass
        self.delta_t = delta_t
        self.angle = radians(initial_angle)
        self.velocity_x = initial_velocity_x
        self.position_x = initial_position_x

    def next(self, angle: float | None = None) -> Tuple[float, float]:
        """
        Calculates the next Position of the ball on the seesaw based on the provided parameters.
        :param angle: Angle of the seesaw in Degree
        :return: (Angle of the seesaw in Degree, Position of the ball on the seesaw)
        """
        # Update Angle if specified
        if angle is not None:
            self.angle = radians(angle)

        # Apply Friction Force only if Element is moving
        friction_force = self.ROLLING_FRICTION_COEFFICIENT * self.GRAVITY_CONSTANT * cos(self.angle) if self.velocity_x != 0 else 0
        # Calculate Acceleration alongside the seesaw
        acceleration_x = (self.GRAVITY_CONSTANT * sin(self.angle) - friction_force) / self.mass

        # Calculate new Velocity and Position
        self.velocity_x += acceleration_x * self.delta_t
        self.position_x += self.velocity_x * self.delta_t

        return degrees(self.angle), self.position_x
