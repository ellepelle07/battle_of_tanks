import pygame
import sys
import math
from gui import Text
import tanks
import recent_winner      # Använd nya recent_winner-modulen
import explosions         # Explosion‑klassen används korrekt här
from enum import Enum
from shared.constants import *

# Inställningar
AIM_LINE_LENGTH      = 320
GROUND_LEVEL         = SCREEN_HEIGHT - 90
G                    = 300   # Gravitation i pixlar/sekund^2
FUEL_BONUS_PER_ROUND = 10    # Bränslebonus varje hel runda
TARGET_AREA_COLOR = (255, 0, 0)

pygame.mixer.init()

# Ladda bakgrundsbild
background_image = pygame.image.load("assets/images/battlefield_background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

T90_IMG = "assets/sprites/T90.png"
T34_IMG = "assets/sprites/T34.png"
M1_ABRAMS_IMG = "assets/sprites/M1_ABRAMS.png"
SHERMAN_IMG =  "assets/sprites/SHERMAN.png"

class GamePhases(Enum):
    MOVE = 1,
    AIM = 2,
    SHOOT = 3

def draw_dashed_line(surface, color, start_pos, end_pos, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = int((dx**2 + dy**2)**0.5)
    dash_count = distance // dash_length

    for i in range(dash_count):
        start_x = x1 + (dx * i / dash_count)
        start_y = y1 + (dy * i / dash_count)
        end_x = x1 + (dx * (i + 0.5) / dash_count)
        end_y = y1 + (dy * (i + 0.5) / dash_count)
        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 3)


def start_battle(selected_tanks, screen):
    battle_sound = pygame.mixer.Sound("assets/sound/battle_sound.ogg")
    engine_sound = pygame.mixer.Sound("assets/sound/engine_sound.mp3")
    battle_sound.play(loops=-1)

    engine_playing = False

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

    left_tank  = create_tank(selected_tanks[0], 100,           GROUND_LEVEL, facing=1)
    right_tank = create_tank(selected_tanks[1], screen_width-200, GROUND_LEVEL, facing=-1)

    current_phase: GamePhases = GamePhases.MOVE
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
        screen.blit(background_image, (0, 0))
        mouse_down_btn = False

        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down_btn = True

        keys = pygame.key.get_pressed()

        # Move
        if current_phase == GamePhases.MOVE:
            active = left_tank if current_player == 1 else right_tank
            if current_player == 1:
                if keys[pygame.K_a]:
                    moved = active.move(-2)
                    if moved and not engine_playing:
                        engine_sound.play(loops=-1)  # Starta loopat ljud
                        engine_playing = True
                if keys[pygame.K_d]:
                    moved = active.move(2)
                    if moved and not engine_playing:
                        engine_sound.play(loops=-1)
                        engine_playing = True
                if not (keys[pygame.K_a] or keys[pygame.K_d]) and engine_playing:
                    engine_sound.stop()
                    engine_playing = False
            else:
                if keys[pygame.K_LEFT]:
                    moved = active.move(-2)
                    if moved and not engine_playing:
                        engine_sound.play(loops=-1)
                        engine_playing = True
                if keys[pygame.K_RIGHT]:
                    moved = active.move(2)
                    if moved and not engine_playing:
                        engine_sound.play(loops=-1)
                        engine_playing = True
                if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and engine_playing:
                    engine_sound.stop()
                    engine_playing = False

            # Aim
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
            draw_dashed_line(screen, WHITE, (sx, sy), (ex, ey), 6)

            # Beräkna och rita landningspunkt
            # sim_dt = 0.02
            # p = active.shoot()
            # sim_x, sim_y = p.x, p.y
            # sim_vx, sim_vy = p.vx, p.vy
            # while sim_y < GROUND_LEVEL:
            #     sim_x += sim_vx * sim_dt
            #     sim_y += sim_vy * sim_dt + 0.5 * G * sim_dt**2
            #     sim_vy += G * sim_dt
            # pygame.draw.circle(screen, TARGET_AREA_COLOR, (int(sim_x), int(sim_y)), 10)

            if keys[pygame.K_SPACE] or mouse_down_btn:
                current_phase = GamePhases.SHOOT

        # Skott
        if current_phase == GamePhases.SHOOT:
            if projectile is None:
                shooter = left_tank if current_player == 1 else right_tank
                projectile = shooter.shoot()

        # Projektiluppdatering
        if projectile:
            projectile.update(dt)
            target = right_tank if current_player == 1 else left_tank
            if target.rect.collidepoint(projectile.x, projectile.y):
                shooter = left_tank if current_player == 1 else right_tank
                target.take_damage(shooter.damage)
                explosions_active.append(explosions.Explosion(projectile.x, projectile.y))
                projectile = None
                current_phase = GamePhases.MOVE
                end_turn()
            elif projectile.is_offscreen(screen_width, screen_height):
                projectile = None
                current_phase = GamePhases.MOVE
                end_turn()

        # Text - anvisning
        if current_phase == GamePhases.MOVE:
            info_text.set_text(f"Spelare {current_player}: Flytta, sikta och tryck SPACE för att skjuta")

        # Rita allt
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

    # Slutscen & spara 'recent winner'
    if left_tank.is_dead():
        winner_name, winner_tank = "Spelare 2", right_tank.name
    elif right_tank.is_dead():
        winner_name, winner_tank = "Spelare 1", left_tank.name
    else:
        winner_name = None

    if winner_name:
        country = "USA" if winner_tank in ("M1 Abrams","Sherman M4A3E8") else "Ryssland"
        recent_winner.save_recent_winner(winner_name, winner_tank, country)

    # Visa vinnarmeddelande
    msg = Text(f"{winner_name or 'Ingen'} vann!", None, 60, BLACK,
               screen_width//2-150, screen_height//2-30)
    screen.fill(WHITE)
    msg.draw(screen)
    pygame.display.flip()
    pygame.time.wait(3000)
    battle_sound.stop()
