Asteroids (Pygame)
===================

A minimalist Asteroids clone built with Python and Pygame.

Features
--------
- Player ship with rotation and thrust (W/S/A/D)
- Shooting with cooldown (Space)
- Wave-based level progression with increasing difficulty
- Asteroids spawn from screen edges and drift inward
- Asteroids split into two smaller on hit
- Screen wrap for player and asteroids
- Shots do not wrap; bullets expire or despawn off-screen
- Scoring with on-screen HUD (small/medium/large: 100/50/20)
- Background image support with animated parallax starfield fallback
 - High score persistence with leader display (saved to `highscore.json`)
 - Name prompt shown when you set a new high score

Requirements
------------
- Python 3.8+
- Pygame (installed via `requirements.txt`)

Setup
-----
1. Create and activate a virtual environment:
   - macOS/Linux: `python3 -m venv venv && source venv/bin/activate`
   - Windows (PowerShell): `py -m venv venv; venv\\Scripts\\Activate.ps1`
2. Install dependencies: `pip install -r requirements.txt`

Run
---
`python main.py`

Controls
--------
- W/S: Thrust forward/backward
- A/D: Rotate left/right
- Space: Shoot

Gameplay Notes
--------------
- Colliding with an asteroid ends the game.
- Bullets expire after ~1.5 seconds.
- Player and asteroids wrap around screen edges; shots do not.

Backgrounds
-----------
- Static image: place `assets/background.png` (auto-scaled to `1280x720`).
- No image: an animated multi-layer parallax starfield is rendered.

Next Ideas
----------
- Lives and respawn
- Sound effects and particle explosions
 - Sound effects and particle explosions

Modes
-----
- Wave mode (default): Spawns a new wave when all asteroids are cleared. Level count and HUD are shown.
- Continuous mode: To switch back to endless spawns, set `ASTEROID_SPAWN_MODE = "continuous"` in `constants.py`.
