import pandas as pd
import pygame as py

from src.visualization.visualization import Visualization
from src.simulation.simulation import Simulation
from src.pid.pidcontroller import PIDController


class PIDVisualization(Visualization):
    def __init__(
            self,
            pid_controller: PIDController,
            simulation: Simulation,
            fps: int,
            initial_angle: float = 0.0,
            initial_position_x: float = 0.0):
        super().__init__(simulation, fps, initial_angle, initial_position_x)
        self.pid_controller = pid_controller

    def run(self):
        ctr = 0
        setpoints = [5] * 20 * 30 + [-5] * 20 * 30
        positions = []
        angles = []
        running = True
        while running:
            self.clock.tick(self.fps)
            self.screen.fill(self.WHITE)

            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                    if event.key == py.K_1:
                        self.marker_position = 0
                    elif event.key == py.K_2:
                        self.marker_position = 1
                    elif event.key == py.K_3:
                        self.marker_position = 2
                    elif event.key == py.K_4:
                        self.marker_position = 3
                    elif event.key == py.K_5:
                        self.marker_position = 4
                    elif event.key == py.K_6:
                        self.marker_position = 5
                    elif event.key == py.K_7:
                        self.marker_position = 6
                    elif event.key == py.K_8:
                        self.marker_position = 7
                    elif event.key == py.K_9:
                        self.marker_position = 8
                    elif event.key == py.K_0:
                        self.is_marker_visible = not self.is_marker_visible

            # Simulate next Step
            angle, velocity, position = self.simulation.next(self.angle)

            # Calculate new angle using the PID-Controller
            # marker_distance = (self.SEESAW_LENGTH / self.SCALE) / (self.num_marker_positions - 1)
            # self.pid_controller.setpoint = self.marker_position * marker_distance - (self.SEESAW_LENGTH / self.SCALE) / 2
            self.pid_controller.setpoint = setpoints[ctr]
            print(self.pid_controller.setpoint, position)
            if ctr == (len(setpoints)) - 2:
                running = False
            new_angle = self.pid_controller.next(position)
            self.angle = new_angle

            positions.append(position)
            angles.append(new_angle)

            # Render Elements
            self.render_seesaw()
            self.render_ball(position * self.SCALE)
            if self.is_marker_visible:
                self.render_marker(self.marker_position)
            self.render_data(angle, velocity, position)

            py.display.flip()

            ctr += 1

        py.quit()
        df = pd.DataFrame({'setpoints': setpoints[:-1], 'positions': positions, 'angles': angles})
        df.to_csv('output.csv', index=False)
