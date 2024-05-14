import pygame as py

from src.simulation import Simulation
from src.visualization.visualization import Visualization


class KeyboardVisualization(Visualization):
    def __init__(
            self,
            simulation: Simulation,
            fps: int, initial_angle: float = 0.0,
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

    def run(self):
        running = True
        while running:
            self.clock.tick(self.fps)
            self.screen.fill(self.WHITE)

            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                elif event.type == py.KEYDOWN:
                    # Change Angle with a and d Key
                    if event.key == py.K_LEFT:
                        if self.angle < 60:
                            self.angle += 3
                    if event.key == py.K_RIGHT:
                        if self.angle > -60:
                            self.angle -= 3

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

            # Simulate next Step
            angle, velocity, position = self.simulation.next(self.angle, self.external_force)

            # Log Data
            self.log(angle, velocity, position)

            # Render Elements
            self.render_seesaw()
            self.render_ball(position * self.SCALE)
            if self.is_marker_visible:
                self.render_marker(self.marker_position)
            self.render_external_force_arrow(self.external_force)
            self.render_data(angle, velocity, position, self.external_force)

            py.display.flip()

        self.save_log()
        py.quit()

