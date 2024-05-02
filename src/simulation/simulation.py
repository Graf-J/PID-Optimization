from math import sin, cos, radians, degrees
from typing import Tuple


class Simulation:
    ROLLING_FRICTION_COEFFICIENT = 0.04
    GRAVITY_CONSTANT = 9.81

    def __init__(
            self,
            mass: float,
            delta_t: float,
            initial_angle: float = 0.0,
            initial_velocity_x: float = 0.0,
            initial_position_x: float = 0.0,
            min_angle: float = -60.0,
            max_angle: float = 60.0,
            max_angle_change: float = 4.0):
        self.mass = mass
        self.delta_t = delta_t
        self._angle = radians(initial_angle)
        self.velocity_x = initial_velocity_x
        self.position_x = initial_position_x
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.max_angle_change = max_angle_change

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, angle: float):
        # Check for Min and Max Angle
        if angle > self.max_angle:
            angle = self.max_angle
        elif angle < self.min_angle:
            angle = self.min_angle

        # Check for Min-Change and Max-Change of Angle
        if angle > (degrees(self.angle) + self.max_angle_change):
            angle = degrees(self.angle) + self.max_angle_change
        elif angle < (degrees(self.angle) - self.max_angle_change):
            angle = degrees(self.angle) - self.max_angle_change

        self._angle = radians(angle)

    def next(self, angle: float | None = None, external_force: float = 0.0) -> Tuple[float, float, float]:
        """
        Calculates the next Position of the ball on the seesaw based on the provided parameters.
        :param external_force: Force of the Wind pushing against the Ball
        :param angle: Angle of the seesaw in Degree
        :return: Angle, Acceleration, Velocity, Position
        """
        # Update Angle if specified
        if angle is not None:
            self.angle = angle

        # Apply Friction Force in corresponding direction
        friction_force = self.ROLLING_FRICTION_COEFFICIENT * self.GRAVITY_CONSTANT * cos(self.angle)
        if self.velocity_x < 0:
            friction_force *= -1

        # Calculate Acceleration alongside the Seesaw based on Gravity Constant
        acceleration_x = -((self.GRAVITY_CONSTANT * sin(self.angle) + friction_force) / self.mass)

        # Add Wind-Force
        acceleration_x += external_force / self.mass

        # Calculate new Velocity and Position
        self.velocity_x += acceleration_x * self.delta_t
        self.position_x += self.velocity_x * self.delta_t

        return degrees(self.angle), self.velocity_x, self.position_x

    def reset(self):
        self.angle = 0.0
        self.velocity_x = 0.0
        self.position_x = 0.0
