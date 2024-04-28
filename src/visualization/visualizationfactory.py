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
        # Create Simulation
        simulation = Simulation(
            mass=mass,
            delta_t=1 / 30,
            initial_angle=initial_angle,
            initial_velocity_x=initial_velocity,
            initial_position_x=initial_position
        )

        # PID-Controller Parameters
        kp = -10
        ki = -0.0002
        kd = -150
        setpoint = 0
        # Create PID-Controller
        pid_controller = PIDController(kp, ki, kd, setpoint)

        # Return Visualization
        if visualization_type == VisualizationType.KEYBOARD:
            return KeyboardVisualization(simulation, fps, initial_angle, initial_position)
        elif visualization_type == VisualizationType.PID:
            return PIDVisualization(pid_controller, simulation, fps, initial_angle, initial_position)
        else:
            raise NotImplementedError('Specified Visualization Type not implemented')
