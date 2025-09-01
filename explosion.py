import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, EXPLOSION_DURATION


class Explosion(pygame.sprite.Sprite):
    """A simple expanding, fading explosion effect.

    Draws a glowing ring with a soft inner flash that expands and fades
    over a short duration, then self-destructs.
    """

    def __init__(self, x: float, y: float, base_radius: int):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.age = 0.0
        self.duration = EXPLOSION_DURATION
        # Scale the visual size with the destroyed asteroid radius
        self.max_radius = max(12, int(base_radius * 1.6))

    def update(self, dt: float):
        self.age += dt
        if self.age >= self.duration:
            self.kill()

    def draw(self, screen: pygame.Surface):
        t = max(0.0, min(1.0, self.age / self.duration))
        radius = int(self.max_radius * t)
        alpha = int(255 * (1.0 - t))
        if radius <= 0 or alpha <= 0:
            return

        size = radius * 2 + 6
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        ring_color = (255, 200, 80, alpha)
        pygame.draw.circle(surf, ring_color, (cx, cy), radius, 3)

        inner_r = max(1, radius // 2)
        glow_color = (255, 120, 40, max(0, alpha // 3))
        pygame.draw.circle(surf, glow_color, (cx, cy), inner_r)

        spokes = 8
        spoke_len = max(2, radius // 3)
        spoke_color = (255, 220, 120, max(0, alpha // 2))
        for i in range(spokes):
            angle = (360 / spokes) * i
            v = pygame.Vector2(0, -1).rotate(angle) * spoke_len
            start = (cx + v.x * 0.4, cy + v.y * 0.4)
            end = (cx + v.x, cy + v.y)
            pygame.draw.line(surf, spoke_color, start, end, 1)

        screen.blit(surf, (self.position.x - cx, self.position.y - cy))

