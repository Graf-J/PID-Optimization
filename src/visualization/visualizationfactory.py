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
        mass = 1
        fps = 60
        initial_angle = 0.0
        initial_velocity_x = 0.0
        initial_position_x = 0.0

        # Create Simulation
        simulation = Simulation(
            mass=mass, delta_t=1 / fps,
            initial_angle=initial_angle,
            initial_position_x=initial_position_x,
            initial_velocity_x=initial_velocity_x
        )

        # Create PID Controller
        pid_controller = PIDController(-3, -0.001, -0.05, 1)

        # Return Visualization
        if visualization_type == VisualizationType.KEYBOARD:
            return KeyboardVisualization(simulation, fps, initial_angle, initial_position_x)
        elif visualization_type == VisualizationType.PID:
            return PIDVisualization(pid_controller, simulation, fps, initial_angle, initial_position_x)
        else:
            raise NotImplementedError('Specified Visualization Type not implemented')
