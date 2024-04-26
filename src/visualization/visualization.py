from math import sin, tan, cos, radians

import pygame
import pygame as py

from src.simulation import Simulation


class SeesawVisualization:
    # Parameters
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    SEESAW_LENGTH = 500
    SEESAW_THICKNESS = 5
    BALL_RADIUS = 20
    SCALE = 7
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    def __init__(self, fps: int = 30, initial_angle: float = 0.0):
        self.fps = fps
        self.angle = initial_angle

        self.screen = None
        self.clock = None

        self.seesaw_surface = None
        self.seesaw_rect = None

        self.ball_surface = None
        self.ball_rect = None

        self.initialize_pygame()
        self.create_seesaw()
        self.create_ball()

    def initialize_pygame(self):
        py.init()
        self.screen = py.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = py.time.Clock()

    def create_seesaw(self):
        self.seesaw_surface = py.Surface((self.SEESAW_LENGTH, self.SEESAW_THICKNESS))
        self.seesaw_surface.set_colorkey(self.WHITE)
        self.seesaw_surface.fill(self.BLACK)

        self.seesaw_rect = self.seesaw_surface.get_rect()
        self.seesaw_rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

    def create_ball(self):
        self.ball_surface = pygame.Surface((self.BALL_RADIUS * 2, self.BALL_RADIUS * 2), py.SRCALPHA)
        pygame.draw.circle(self.ball_surface, self.BLUE, (self.BALL_RADIUS, self.BALL_RADIUS), self.BALL_RADIUS)

    def render_seesaw(self):
        temp_center = self.seesaw_rect.center
        new_seesaw_surface = py.transform.rotate(self.seesaw_surface, self.angle)

        new_seesaw_rect = new_seesaw_surface.get_rect()
        new_seesaw_rect.center = temp_center

        self.screen.blit(new_seesaw_surface, new_seesaw_rect)

    def render_ball(self, ball_position_x: float):
        # Calculate Ball Position based on seesaw angle
        ball_x = self.SCREEN_WIDTH // 2 + ball_position_x - self.BALL_RADIUS * sin(radians(self.angle))
        ball_y = self.SCREEN_HEIGHT // 2 - ball_position_x * tan(radians(self.angle)) - self.BALL_RADIUS * cos(radians(self.angle))

        ball_rect = self.ball_surface.get_rect(center=(ball_x, ball_y))

        self.screen.blit(self.ball_surface, ball_rect)

    def run(self):
        simulation = Simulation(mass=1, delta_t=1 / self.fps, initial_angle=self.angle)

        running = True
        while running:

            self.clock.tick(self.fps)
            self.screen.fill(self.WHITE)

            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == py.K_LEFT:
                        self.angle += 2
                    elif event.key == py.K_RIGHT:
                        self.angle -= 2

            _, ball_position_x = simulation.next(self.angle)

            self.render_seesaw()
            self.render_ball(ball_position_x * self.SCALE)

            py.display.flip()

        py.quit()
