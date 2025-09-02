import pygame
from constants import (
    ASTEROID_KINDS,
    LEVEL_START_ASTEROIDS,
    LEVEL_ASTEROIDS_INCREMENT,
    LEVEL_SPEED_INCREASE,
    LEVEL_INTERMISSION,
)


class LevelManager:

    def __init__(self, asteroid_field, asteroids_group):
        self.asteroid_field = asteroid_field
        self.asteroids_group = asteroids_group

        self.level = 0
        self.state = "intermission"
        self.timer = 0.0
        self._start_next_level()

    def update(self, dt: float):
        if self.state == "playing":
            if len(self.asteroids_group.sprites()) == 0:
                self.state = "intermission"
                self.timer = 0.0
        else:
            self.timer += dt
            if self.timer >= LEVEL_INTERMISSION:
                self._start_next_level()

    def _start_next_level(self):
        self.level += 1
        self.state = "playing"
        self.timer = 0.0

        count = LEVEL_START_ASTEROIDS + (self.level - 1) * LEVEL_ASTEROIDS_INCREMENT
        speed_mult = 1.0 + (self.level - 1) * LEVEL_SPEED_INCREASE

        for _ in range(count):
            self.asteroid_field.spawn_random(kind=ASTEROID_KINDS, speed_mult=speed_mult)
