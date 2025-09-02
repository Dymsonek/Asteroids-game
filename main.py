import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from starfield import Starfield
from explosion import Explosion
from levelmanager import LevelManager
from highscores import load_highscore, save_highscore


def prompt_for_name(screen: pygame.Surface, font: pygame.font.Font, default: str = "") -> str:
    """Modal text input for player name.

    Returns the entered name (or "Player" on ESC/empty). Blocks game loop until done.
    """
    name = default
    blink = 0
    clock = pygame.time.Clock()
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return name.strip() or "Player"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() or "Player"
                if event.key == pygame.K_ESCAPE:
                    return "Player"
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    ch = event.unicode
                    if ch and ch.isprintable() and ch not in "\r\n\t":
                        if len(name) < 16:
                            name += ch

        # Draw semi-transparent overlay on top of current frame
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Prompt box
        title = font.render("New High Score!", True, pygame.Color("white"))
        prompt = font.render("Enter your name:", True, pygame.Color("white"))
        entered = name + ("_" if (blink // 30) % 2 == 0 else "")
        input_surf = font.render(entered, True, pygame.Color("yellow"))
        hint = font.render("Enter to save · Esc to cancel", True, pygame.Color("gray"))

        # Center vertically
        y = SCREEN_HEIGHT // 2 - 40
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, y)))
        y += 40
        screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, y)))
        y += 40
        screen.blit(input_surf, input_surf.get_rect(center=(SCREEN_WIDTH // 2, y)))
        y += 40
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, y)))

        pygame.display.flip()
        blink = (blink + 1) % 120
        clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
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
    Explosion.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    score = 0
    leader_name, high_score = load_highscore()
    # Track a live display high separate from saved high for HUD feedback
    hud_high = high_score
    new_high_pending = False
    level_mgr = LevelManager(asteroid_field, asteroids)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        level_mgr.update(dt)

        for asteroid in list(asteroids):
            if asteroid.collides_with(player):
                # If it's a new high score, prompt for a name and persist
                if score > high_score:
                    try:
                        name = prompt_for_name(screen, font, default=leader_name or "")
                    except Exception:
                        name = "Player"
                    leader_name = name
                    high_score = score
                    try:
                        save_highscore(leader_name, high_score)
                        print(f"New high score saved: {high_score} by {leader_name}")
                    except Exception as e:
                        print(f"Failed to save high score: {e}")
                print("Game over!")
                sys.exit()

            for shot in list(shots):
                if asteroid.collides_with(shot):
                    shot.kill()
                    score += asteroid.get_score_value()
                    asteroid.split()
                    # Update live HUD high (do not persist until game over)
                    if score > hud_high:
                        hud_high = score
                        new_high_pending = True

        if background_surface is not None:
            screen.blit(background_surface, (0, 0))
        else:
            screen.fill("black")
            starfield.update(dt)
            starfield.draw(screen)

        for obj in drawable:
            obj.draw(screen)

        score_surf = font.render(f"Score: {score}", True, pygame.Color("white"))
        level_surf = font.render(f"Level: {level_mgr.level}", True, pygame.Color("white"))
        if new_high_pending:
            leader_label = f"High: {hud_high} (You)"
        else:
            leader_label = f"High: {high_score}"
            if leader_name:
                leader_label += f" ({leader_name})"
        high_surf = font.render(leader_label, True, pygame.Color("white"))

        screen.blit(score_surf, (10, 10))
        screen.blit(level_surf, (10, 40))
        # Place high score at top-right with small padding
        hs_rect = high_surf.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(high_surf, hs_rect)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
