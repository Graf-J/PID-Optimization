from abc import ABC, abstractmethod
from math import sin, tan, cos, radians

import pygame
import pygame as py

from src.simulation import Simulation


class Visualization(ABC):
    # Parameters
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    SEESAW_LENGTH = 500
    SEESAW_THICKNESS = 10
    BALL_RADIUS = 20
    SCALE = 20
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    def __init__(
            self,
            simulation: Simulation,
            fps: int,
            initial_angle: float,
            initial_position_x: float,
            initial_external_force: float,
            max_external_force: float):
        self.simulation = simulation
        self.fps = fps
        self.angle = initial_angle
        self.initial_position_x = initial_position_x
        self.external_force = initial_external_force
        self.max_external_force = max_external_force
        self.max_external_force = 3.0
        self.marker_position = 4
        self.is_marker_visible = False
        self.num_marker_positions = 9

        self.screen = None
        self.clock = None
        self.font = None

        self.seesaw_surface = None
        self.seesaw_rect = None

        self.ball_surface = None
        self.ball_rect = None

        self.marker_surface = None
        self.marker_rect = None

        self.initialize_pygame()
        self.create_seesaw()
        self.create_ball()
        self.create_marker()

    def initialize_pygame(self):
        py.init()
        self.screen = py.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = py.time.Clock()
        self.font = pygame.font.SysFont('arial.ttf', 30)
        py.display.set_caption('Simulation')

    def create_seesaw(self):
        self.seesaw_surface = py.Surface((self.SEESAW_LENGTH, self.SEESAW_THICKNESS))
        self.seesaw_surface.set_colorkey(self.WHITE)
        self.seesaw_surface.fill(self.BLACK)

        self.seesaw_rect = self.seesaw_surface.get_rect()
        self.seesaw_rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

    def create_ball(self):
        self.ball_surface = pygame.Surface((self.BALL_RADIUS * 2, self.BALL_RADIUS * 2), py.SRCALPHA)
        pygame.draw.circle(self.ball_surface, self.BLUE, (self.BALL_RADIUS, self.BALL_RADIUS), self.BALL_RADIUS)

    def create_marker(self):
        self.marker_surface = py.Surface((self.SEESAW_THICKNESS, self.SEESAW_THICKNESS))
        self.marker_surface.set_colorkey(self.WHITE)
        self.marker_surface.fill(self.RED)

        self.marker_rect = self.marker_surface.get_rect()
        self.marker_rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

    def render_seesaw(self):
        temp_center = self.seesaw_rect.center
        new_seesaw_surface = py.transform.rotate(self.seesaw_surface, self.angle)

        new_seesaw_rect = new_seesaw_surface.get_rect()
        new_seesaw_rect.center = temp_center

        self.screen.blit(new_seesaw_surface, new_seesaw_rect)

    def render_ball(self, ball_position_x: float):
        ball_x = self.SCREEN_WIDTH // 2 + ball_position_x - (self.BALL_RADIUS + self.SEESAW_THICKNESS / 2) * sin(
            radians(self.angle))
        ball_y = self.SCREEN_HEIGHT // 2 - ball_position_x * tan(radians(self.angle)) - (
                    self.BALL_RADIUS + self.SEESAW_THICKNESS / 2) * cos(radians(self.angle))

        ball_rect = self.ball_surface.get_rect(center=(ball_x, ball_y))

        self.screen.blit(self.ball_surface, ball_rect)

    def render_marker(self, position: int):
        marker_distance = self.SEESAW_LENGTH / (self.num_marker_positions - 1)

        marker_position_relative_to_seesaw_center = position * marker_distance - self.SEESAW_LENGTH // 2
        marker_x = marker_position_relative_to_seesaw_center * cos(radians(self.angle)) + self.SCREEN_WIDTH // 2
        marker_y = self.SCREEN_HEIGHT // 2 - (marker_x - self.SCREEN_WIDTH // 2) * tan(radians(self.angle))

        new_marker_surface = py.transform.rotate(self.marker_surface, self.angle)

        new_marker_rect = new_marker_surface.get_rect()
        new_marker_rect.center = (marker_x, marker_y)

        self.screen.blit(new_marker_surface, new_marker_rect)

    def render_external_force_arrow(self, external_force: float):
        max_arrow_height = 120
        min_arrow_height = 20
        arrow_height_range = max_arrow_height - min_arrow_height
        arrow_height = min_arrow_height + (abs(external_force) / self.max_external_force) * arrow_height_range

        if external_force > 0:
            arrow_x = 10
        elif external_force < 0:
            arrow_x = self.SCREEN_WIDTH - 10
        else:
            return

        arrow_y = (self.SCREEN_HEIGHT - arrow_height) // 2
        if external_force > 0:
            pygame.draw.polygon(self.screen, self.BLACK, ((arrow_x, arrow_y + arrow_height * 0.33),
                                                          (arrow_x, arrow_y + arrow_height * 0.66),
                                                          (arrow_x + arrow_height * 0.6,
                                                           arrow_y + arrow_height * 0.66),
                                                          (arrow_x + arrow_height * 0.6,
                                                           arrow_y + arrow_height),
                                                          (arrow_x + arrow_height * 1.2,
                                                           arrow_y + arrow_height * 0.5),
                                                          (arrow_x + arrow_height * 0.6,
                                                           arrow_y),
                                                          (arrow_x + arrow_height * 0.6,
                                                           arrow_y + arrow_height * 0.33)))
        elif external_force < 0:
            pygame.draw.polygon(self.screen, self.BLACK, ((arrow_x, arrow_y + arrow_height * 0.33),
                                                          (arrow_x, arrow_y + arrow_height * 0.66),
                                                          (arrow_x - arrow_height * 0.6,
                                                           arrow_y + arrow_height * 0.66),
                                                          (arrow_x - arrow_height * 0.6,
                                                           arrow_y + arrow_height),
                                                          (arrow_x - arrow_height * 1.2,
                                                           arrow_y + arrow_height * 0.5),
                                                          (arrow_x - arrow_height * 0.6,
                                                           arrow_y),
                                                          (arrow_x - arrow_height * 0.6,
                                                           arrow_y + arrow_height * 0.33)))

    def render_data(self, angle: float, velocity: float, position: float, external_force: float):
        # Prevent annoying fluctuations because of rolling friction coefficient
        if abs(velocity) < 0.01:
            velocity = 0

        # Render Angle
        angle_text_surface = self.font.render(f'Angle: {round(angle, 2)}°', True, self.BLACK)
        self.screen.blit(angle_text_surface, (10, 10))
        # Render Velocity
        angle_text_surface = self.font.render(f'Velocity: {round(velocity, 2)} m/s', True, self.BLACK)
        self.screen.blit(angle_text_surface, (10, 40))
        # Render Position
        angle_text_surface = self.font.render(f'Position: {round(position, 2)} m', True, self.BLACK)
        self.screen.blit(angle_text_surface, (10, 70))
        # Render External Force
        external_force_text_surface = self.font.render(f'External Force: {round(external_force, 2)} N', True,
                                                       self.BLACK)
        self.screen.blit(external_force_text_surface, (10, 100))

    @abstractmethod
    def run(self):
        pass
