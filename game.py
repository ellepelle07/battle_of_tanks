import pygame
import sys
import math
from gui import Text
import tanks
import recent_winner      # Använd nya recent_winner-modulen
import explosions         # Explosion‑klassen används korrekt här

# Färger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# Skärmstorlek
SCREEN_WIDTH  = 1450
SCREEN_HEIGHT = 700

# Inställningar
AIM_LINE_LENGTH      = 350
GROUND_LEVEL         = SCREEN_HEIGHT - 90
G                    = 300   # Gravitation i pixlar/sekund^2
FUEL_BONUS_PER_ROUND = 10    # Bränslebonus varje hel runda

# Ladda bakgrundsbild
background_image = pygame.image.load("assets/images/battlefield_background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

T90_IMG = "assets/sprites/T90.png"
T34_IMG = "assets/sprites/T34.png"
M1_ABRAMS_IMG = "assets/sprites/M1_ABRAMS.png"
SHERMAN_IMG =  "assets/sprites/SHERMAN.png"

def start_battle(selected_tanks, screen):
    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()

    def create_tank(name, x, bottom_y, facing):
        # Sätt HP, damage och bränsle beroende på tank
        if name in ("M1 Abrams", "T-90"):
            hp   = 210
            dmg  = 25
            fuel = 250
            img  = M1_ABRAMS_IMG if name == "M1 Abrams" else T90_IMG
        else:
            hp   = 155
            dmg  = 50
            fuel = 150
            img  = SHERMAN_IMG if name.startswith("Sherman") else T34_IMG

        # Skapa tank och ge den max_fuel
        t = tanks.Tank(
            name=name,
            max_hp=hp,
            damage=dmg,
            x=x, y=bottom_y,
            image_path=img,
            facing=facing,
            max_fuel=fuel
        )
        t.rect.bottom = bottom_y
        t.x = t.rect.centerx
        return t

    left_tank  = create_tank(selected_tanks[0], 100,            GROUND_LEVEL, facing=1)
    right_tank = create_tank(selected_tanks[1], screen_width-200, GROUND_LEVEL, facing=-1)

    current_phase     = "move"
    current_player    = 1
    projectile        = None
    explosions_active = []

    round_counter    = 1
    turns_in_round   = 0

    info_text = Text("", None, 30, BLACK, 50, 20)

    def end_turn():
        nonlocal current_player, turns_in_round, round_counter
        # Växla spelare
        current_player = 2 if current_player == 1 else 1
        turns_in_round += 1
        # Efter båda spelare turats om, ge bränslebonus
        if turns_in_round >= 2:
            round_counter  += 1
            turns_in_round  = 0
            left_tank.fuel  = min(left_tank.max_fuel,  left_tank.fuel  + FUEL_BONUS_PER_ROUND)
            right_tank.fuel = min(right_tank.max_fuel, right_tank.fuel + FUEL_BONUS_PER_ROUND)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # ======== MOVE ========
        if current_phase == "move":
            active = left_tank if current_player == 1 else right_tank
            if current_player == 1:
                if keys[pygame.K_a]:
                    active.move(-2)
                if keys[pygame.K_d]:
                    active.move(2)
            else:
                if keys[pygame.K_LEFT]:
                    active.move(-2)
                if keys[pygame.K_RIGHT]:
                    active.move(2)
            if keys[pygame.K_RETURN]:
                current_phase = "aim"

        # ======== AIM ========
        elif current_phase == "aim":
            active = left_tank if current_player == 1 else right_tank
            mx, my = pygame.mouse.get_pos()
            dx = mx - active.rect.centerx
            dy = active.rect.centery - my
            raw = math.degrees(math.atan2(dy, dx))
            if raw < 0: raw += 360
            if current_player == 1:
                active.angle = max(0, min(90, raw))
            else:
                active.angle = max(90, min(180, raw))

            # Rita siktlinje
            rad = math.radians(active.angle)
            sx, sy = active.rect.center
            ex = sx + AIM_LINE_LENGTH * math.cos(rad)
            ey = sy - AIM_LINE_LENGTH * math.sin(rad)
            pygame.draw.line(screen, WHITE, (sx, sy), (ex, ey), 3)

            # Beräkna och rita landningspunkt
            sim_dt = 0.02
            p = active.shoot()
            sim_x, sim_y = p.x, p.y
            sim_vx, sim_vy = p.vx, p.vy
            while sim_y < GROUND_LEVEL:
                sim_x += sim_vx * sim_dt
                sim_y += sim_vy * sim_dt + 0.5 * G * sim_dt**2
                sim_vy += G * sim_dt
            pygame.draw.circle(screen, RED, (int(sim_x), int(sim_y)), 10)

            if keys[pygame.K_RETURN]:
                current_phase = "shoot"

        # ======== SHOOT ========
        elif current_phase == "shoot":
            if keys[pygame.K_SPACE] and projectile is None:
                shooter = left_tank if current_player == 1 else right_tank
                projectile = shooter.shoot()

        # ======== PROJEKTIL-UPPDATE ========
        if projectile:
            projectile.update(dt)
            target = right_tank if current_player == 1 else left_tank
            if target.rect.collidepoint(projectile.x, projectile.y):
                shooter = left_tank if current_player == 1 else right_tank
                target.take_damage(shooter.damage)
                explosions_active.append(explosions.Explosion(projectile.x, projectile.y))
                projectile = None
                current_phase = "move"
                end_turn()
            elif projectile.is_offscreen(screen_width, screen_height):
                projectile = None
                current_phase = "move"
                end_turn()

        # ======== TEXT-ANVISNING ========
        if current_phase == "move":
            info_text.set_text(f"Spelare {current_player}: Flytta (ENTER för sikta)")
        elif current_phase == "aim":
            info_text.set_text(f"Spelare {current_player}: Rikta – ENTER för skjut")
        else:
            info_text.set_text(f"Spelare {current_player}: Tryck SPACE")

        # ======== RITA ALLT ========
        screen.blit(background_image, (0, 0))
        left_tank.draw(screen)
        right_tank.draw(screen)

        if projectile:
            projectile.draw(screen)

        for ex in explosions_active:
            ex.update(dt)
            ex.draw(screen)
            if ex.finished:
                explosions_active.remove(ex)

        # Runda & bränsle‐info
        Text(f"Runda: {round_counter}",  None, 30, BLACK, SCREEN_WIDTH-150, 20).draw(screen)
        Text(f"Bränsle P1: {int(left_tank.fuel)}",  None, 24, BLACK, 20, 50).draw(screen)
        Text(f"Bränsle P2: {int(right_tank.fuel)}", None, 24, BLACK, SCREEN_WIDTH-160, 50).draw(screen)

        info_text.draw(screen)
        pygame.display.flip()

        if left_tank.is_dead() or right_tank.is_dead():
            running = False

    # ======== SLUTSCEN & SPARA RECENT WINNER ========
    if left_tank.is_dead():
        winner_name, winner_tank = "Spelare 2", right_tank.name
    elif right_tank.is_dead():
        winner_name, winner_tank = "Spelare 1", left_tank.name
    else:
        winner_name = None

    if winner_name:
        country = "USA" if winner_tank in ("M1 Abrams","Sherman M4A3E8") else "Sovjet"
        recent_winner.save_recent_winner(winner_name, winner_tank, country)

    # Visa vinnarmeddelande
    msg = Text(f"{winner_name or 'Ingen'} vann!", None, 60, BLACK,
               screen_width//2-150, screen_height//2-30)
    screen.fill(WHITE)
    msg.draw(screen)
    pygame.display.flip()
    pygame.time.wait(3000)
