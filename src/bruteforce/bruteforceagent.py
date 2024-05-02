from typing import List, Callable

from src.simulation import Simulation
from src.pid import PIDController


class BruteForceAgent:
    def __init__(self, simulation: Simulation, pid_controller: PIDController, error_fun: Callable):
        self.simulation = simulation
        self.pid_controller = pid_controller
        self.error_fun = error_fun

    def run(self, setpoints: List[float], external_force: List[float], weight_factor: float):
        positions = []
        position = 0
        for idx, _ in enumerate(setpoints):
            self.pid_controller.setpoint = setpoints[idx]
            new_angle = self.pid_controller.next(position)
            _, _, position = self.simulation.next(new_angle, external_force[idx])
            positions.append(position)

        error = self.error_fun(positions, setpoints, weight_factor=weight_factor)

        return error, positions
