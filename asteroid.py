import pygame
import random
from constants import *
from circleshape import CircleShape
from explosion import Explosion


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self._shape = self._generate_shape()
        # Rotation state
        self.rotation = random.uniform(0, 360)
        spin = random.uniform(-ASTEROID_MAX_SPIN, ASTEROID_MAX_SPIN)
        if abs(spin) < ASTEROID_MIN_SPIN:
            spin = ASTEROID_MIN_SPIN if spin >= 0 else -ASTEROID_MIN_SPIN
        self.spin = spin

    def draw(self, screen):
        pts = []
        for (px, py) in self._shape:
            v = pygame.Vector2(px, py).rotate(self.rotation)
            pts.append((self.position.x + v.x, self.position.y + v.y))
        pygame.draw.polygon(screen, "white", pts, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation = (self.rotation + self.spin * dt) % 360
        self.wrap_position()

    def split(self):
        Explosion(self.position.x, self.position.y, self.radius)
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2

    def get_score_value(self):
        kind = int(self.radius / ASTEROID_MIN_RADIUS)
        return ASTEROID_POINTS.get(kind, 0)

    def _generate_shape(self):
        vertex_count = random.randint(10, 16)
        pts = []
        for i in range(vertex_count):
            angle = (360 / vertex_count) * i + random.uniform(-6, 6)
            # Keep within circle: jitter between 70% and 100% of radius
            r = self.radius * random.uniform(0.7, 1.0)
            v = pygame.Vector2(0, -r).rotate(angle)
            pts.append((v.x, v.y))
        return pts
