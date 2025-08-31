import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Starfield:
    """Animated multi-layer parallax starfield.

    Layers move at different speeds to create a depth effect.
    Used when no background image is provided.
    """

    def __init__(self):
        # Define three layers: far, mid, near
        # Each tuple: (count, speed_pixels_per_sec, size_choices)
        self.layers_spec = [
            (160, 12, [1, 1, 1, 1, 2]),   # far: many, slow, small
            (90, 24, [1, 2, 2]),          # mid: medium amount/speed/size
            (45, 48, [2, 2, 3]),          # near: few, faster, larger
        ]

        self.layers = []  # list of lists of stars
        for count, speed, sizes in self.layers_spec:
            stars = []
            for _ in range(count):
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(SCREEN_HEIGHT)
                radius = random.choice(sizes)
                shade = random.randint(160, 255)
                color = (shade, shade, shade)
                stars.append([x, y, radius, color, speed])
            self.layers.append(stars)

    def update(self, dt: float):
        for stars in self.layers:
            for s in stars:
                # s: [x, y, r, color, speed]
                s[1] += s[4] * dt
                r = s[2]
                if s[1] > SCREEN_HEIGHT + r:
                    s[1] = -r
                    s[0] = random.randrange(SCREEN_WIDTH)

    def draw(self, screen: pygame.Surface):
        # Draw in order: far -> near
        for stars in self.layers:
            for x, y, r, color, _ in stars:
                pygame.draw.circle(screen, color, (int(x), int(y)), r)

