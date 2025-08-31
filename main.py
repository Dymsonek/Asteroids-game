import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from starfield import Starfield


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Load background image if present; otherwise use animated parallax starfield
    try:
        bg = pygame.image.load("assets/background.png").convert()
        background_surface = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        starfield = None
    except Exception:
        background_surface = None
        starfield = Starfield()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in list(asteroids):
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()

            for shot in list(shots):
                if asteroid.collides_with(shot):
                    shot.kill()
                    score += asteroid.get_score_value()
                    asteroid.split()

        if background_surface is not None:
            screen.blit(background_surface, (0, 0))
        else:
            screen.fill("black")
            starfield.update(dt)
            starfield.draw(screen)

        for obj in drawable:
            obj.draw(screen)

        # Draw HUD
        score_surf = font.render(f"Score: {score}", True, pygame.Color("white"))
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
