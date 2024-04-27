from src.visualization.visualizationtype import VisualizationType
from src.visualization.visualization import Visualization
from src.visualization.keyboardvisualization import KeyboardVisualization
from src.visualization.pidvisualization import PIDVisualization
from src.simulation import Simulation


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

        # Return Visualization
        if visualization_type == VisualizationType.KEYBOARD:
            return KeyboardVisualization(simulation, fps, initial_angle, initial_position_x)
        elif visualization_type == VisualizationType.PID:
            NotImplementedError()
        else:
            raise NotImplementedError('Specified Visualization Type not implemented')
