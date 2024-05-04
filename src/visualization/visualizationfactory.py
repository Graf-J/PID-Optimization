from src.visualization.visualizationtype import VisualizationType
from src.visualization.visualization import Visualization
from src.visualization.keyboardvisualization import KeyboardVisualization
from src.visualization.pidvisualization import PIDVisualization
from src.simulation import Simulation
from src.pid import PIDController


class VisualizationFactory:
    @staticmethod
    def create_visualization(visualization_type: VisualizationType) -> Visualization:
        # Simulation Parameters
        fps = 30
        mass = 0.2
        initial_angle = 0.0
        initial_velocity = 0.0
        initial_position = 0.0
        initial_external_force = 0.0
        max_external_force = 2.5
        min_angle = -60.0
        max_angle = 60.0
        max_angle_change = 4.0
        # Create Simulation
        simulation = Simulation(
            mass=mass,
            delta_t=1 / 30,
            initial_angle=initial_angle,
            initial_velocity_x=initial_velocity,
            initial_position_x=initial_position,
            min_angle=min_angle,
            max_angle=max_angle,
            max_angle_change=max_angle_change
        )

        # PID-Controller Parameters
        kp = -8.8
        ki = -0.018
        kd = -220
        setpoint = 0
        # Create PID-Controller
        pid_controller = PIDController(kp, ki, kd, setpoint)

        # Return Visualization
        if visualization_type == VisualizationType.KEYBOARD:
            return KeyboardVisualization(
                simulation,
                fps,
                initial_angle,
                initial_position,
                initial_external_force,
                max_external_force
            )
        elif visualization_type == VisualizationType.PID:
            return PIDVisualization(
                pid_controller,
                simulation,
                fps,
                initial_angle,
                initial_position,
                initial_external_force,
                max_external_force
            )
        else:
            raise NotImplementedError('Specified Visualization Type not implemented')
