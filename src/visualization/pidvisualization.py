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
            initial_position_x: float = 0.0,
            initial_external_force: float = 0.0,
            max_external_force: float = 2.5,
            log_data: bool = False,
            log_filename: str = 'data.csv'):
        super().__init__(
            simulation,
            fps,
            initial_angle,
            initial_position_x,
            initial_external_force,
            max_external_force,
            log_data,
            log_filename)
        self.pid_controller = pid_controller

    def render_pid_data(self):
        # Render P-Term
        p_text_surface = self.font.render(f'P: {self.pid_controller.kp}', True, (0, 0, 0))
        self.screen.blit(p_text_surface, (10, self.SCREEN_HEIGHT - 90))
        # Render I-Term
        i_text_surface = self.font.render(f'I:  {self.pid_controller.ki}', True, (0, 0, 0))
        self.screen.blit(i_text_surface, (10, self.SCREEN_HEIGHT - 60))
        # Render D-Term
        d_text_surface = self.font.render(f'D: {self.pid_controller.kd}', True, (0, 0, 0))
        self.screen.blit(d_text_surface, (10, self.SCREEN_HEIGHT - 30))

    def run(self):
        running = True
        position = self.initial_position_x
        while running:
            self.clock.tick(self.fps)
            self.screen.fill(self.WHITE)

            # Listen on Keypress-Events
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                elif event.type == py.KEYDOWN:
                    # Change External Force with Arrow-Keys
                    if event.key == py.K_a:
                        if (self.external_force - 0.5) > -self.max_external_force:
                            self.external_force -= 0.5
                    if event.key == py.K_d:
                        if (self.external_force + 0.5) < self.max_external_force:
                            self.external_force += 0.5

                    # Place Position-Marker
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

            # Calculate new angle using the PID-Controller
            marker_distance = (self.SEESAW_LENGTH / self.SCALE) / (self.num_marker_positions - 1)
            self.pid_controller.setpoint = self.marker_position * marker_distance - (self.SEESAW_LENGTH / self.SCALE) / 2
            new_angle = self.pid_controller.next(position)

            # Simulate next Step
            angle, velocity, position = self.simulation.next(new_angle, self.external_force)
            self.angle = angle

            # Log Data
            self.log(angle, velocity, position)

            # Render Elements
            self.render_seesaw()
            self.render_ball(position * self.SCALE)
            if self.is_marker_visible:
                self.render_marker(self.marker_position)
            self.render_external_force_arrow(self.external_force)
            self.render_data(angle, velocity, position, self.external_force)
            self.render_pid_data()

            py.display.flip()

        self.save_log()
        py.quit()
