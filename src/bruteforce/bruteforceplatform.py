from typing import List, Tuple, Callable

from src.simulation import Simulation
from src.pid import PIDController
from src.bruteforce.bruteforceagent import BruteForceAgent


class BruteForcePlatform:
    @staticmethod
    def execute(pid_args: Tuple[float, float, float], mass: float, delta_t, setpoints: List[float], external_force: List[float], error_fun: Callable, weight_factor: float):
        kp, ki, kd = pid_args
        simulation = Simulation(mass=mass, delta_t=delta_t)
        pid_controller = PIDController(kp, ki, kd, setpoints[0])
        agent = BruteForceAgent(simulation, pid_controller, error_fun)
        error, positions = agent.run(setpoints, external_force, weight_factor)

        return kp, ki, kd, error, positions
