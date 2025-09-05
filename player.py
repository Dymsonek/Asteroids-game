import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.weapon = "single"
        self.weapon_switch_timer = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        self.weapon_switch_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_1]:
            self.weapon = "single"
        if keys[pygame.K_2]:
            self.weapon = "spread"
        if keys[pygame.K_3]:
            self.weapon = "rapid"
        
        self.wrap_position()

    def shoot(self):
        if self.shoot_timer > 0:
            return
        if self.weapon == "rapid":
            self.shoot_timer = PLAYER_RAPID_COOLDOWN
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = forward * PLAYER_SHOOT_SPEED
        elif self.weapon == "spread":
            self.shoot_timer = PLAYER_SPREAD_COOLDOWN
            base = self.rotation
            angles = []
            if PLAYER_SPREAD_COUNT <= 1:
                angles = [0]
            elif PLAYER_SPREAD_COUNT == 2:
                angles = [-PLAYER_SPREAD_ANGLE / 2, PLAYER_SPREAD_ANGLE / 2]
            else:
                mid = PLAYER_SPREAD_COUNT // 2
                for i in range(-mid, mid + 1):
                    if PLAYER_SPREAD_COUNT % 2 == 0 and i == 0:
                        continue
                    angles.append(i * PLAYER_SPREAD_ANGLE)
            for a in angles:
                v = pygame.Vector2(0, 1).rotate(base + a)
                s = Shot(self.position.x, self.position.y)
                s.velocity = v * PLAYER_SHOOT_SPEED
        else:
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = forward * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
