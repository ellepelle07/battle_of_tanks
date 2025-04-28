import pygame
import sys
import math
from gui import Text
import tanks
import recent_winner
import explosions
from enum import Enum
from shared.constants import *
from IcePuddle import IcePuddle
from random import randint

# Inställningar
AIM_LINE_LENGTH = 320
GROUND_LEVEL = SCREEN_HEIGHT - 90
#########GRAVITY = 6000   # Gravitation i pixlar/sekund^2
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


class Battle:
    def __init__(self, screen, selected_tanks):
        self.screen = screen
        self.battle_sound = pygame.mixer.Sound("assets/sound/battle_sound.ogg")
        self.engine_sound = pygame.mixer.Sound("assets/sound/engine_sound.mp3")
        self.engine_playing = False
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = screen.get_size()
        self.puddle = IcePuddle((self.screen_width // 2, GROUND_LEVEL))
        self.current_phase: GamePhases = GamePhases.MOVE
        self.current_player = randint(1, 2)  # Slumpa vilken spelar som börjar
        self.projectile = None
        self.explosions_active = []
        self.round_counter = 1
        self.turns_in_round = 0
        self.info_text = Text("", None, 30, BLACK, 50, 20)
        self.left_tank  = self.__create_tank(selected_tanks[0], 100, GROUND_LEVEL, facing=1)
        self.right_tank = self.__create_tank(selected_tanks[1], self.screen_width-200, GROUND_LEVEL, facing=-1)

    def __create_tank(self, name, x, bottom_y, facing):
        # Sätt HP, damage och bränsle beroende på tank
        if name in ("M1 Abrams", "T-90"):
            hp   = 210
            dmg  = 500
            fuel = 400
            img  = M1_ABRAMS_IMG if name == "M1 Abrams" else T90_IMG
        else:
            hp   = 155
            dmg  = 500
            fuel = 200
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

    def __end_turn(self):
        # Växla spelare
        self.current_player = 2 if self.current_player == 1 else 1
        self.turns_in_round += 1
        # Efter båda spelare turats om, ge bränslebonus
        if self.turns_in_round >= 2:
            self.round_counter  += 1
            self.turns_in_round  = 0
            self.left_tank.fuel  = min(self.left_tank.max_fuel,  self.left_tank.fuel  + FUEL_BONUS_PER_ROUND)
            self.right_tank.fuel = min(self.right_tank.max_fuel, self.right_tank.fuel + FUEL_BONUS_PER_ROUND)

    def start(self):
        self.battle_sound.play(loops=-1)
        running = True
        while running:
            mouse_down_btn = False
            active_tank = self.left_tank if self.current_player == 1 else self.right_tank
            self.screen.blit(background_image, (0, 0))
            self.puddle.draw(self.screen)

            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down_btn = True

            keys = pygame.key.get_pressed()

            # MOVE-fasen
            if self.current_phase == GamePhases.MOVE:
                moved = False
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    moved = active_tank.move(-1)
                    if self.puddle.collides_with(active_tank.rect):
                        moved = active_tank.move(1)
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    moved = active_tank.move(1)
                    if self.puddle.collides_with(active_tank.rect):
                        moved = active_tank.move(-1)

                if moved:  # Om rörelsen lyckades
                    if not self.engine_playing:
                        self.engine_sound.play(loops=-1)  # Starta motorljudet
                        self.engine_playing = True
                else:
                    # Stoppa motorljudet om ingen tangent trycks
                    if self.engine_playing:
                        self.engine_sound.stop()
                        self.engine_playing = False

                # Aim
                mx, my = pygame.mouse.get_pos()
                dx = mx - active_tank.rect.centerx
                dy = active_tank.rect.centery - my
                raw = math.degrees(math.atan2(dy, dx))
                if raw < 0: raw += 360
                if self.current_player == 1:
                    active_tank.angle = max(0, min(90, int(raw)))
                else:
                    active_tank.angle = max(90, min(180, int(raw)))

                # Rita siktlinje
                rad = math.radians(active_tank.angle)
                sx, sy = active_tank.rect.center
                ex = sx + AIM_LINE_LENGTH * math.cos(rad)
                ey = sy - AIM_LINE_LENGTH * math.sin(rad)
                draw_dashed_line(self.screen, WHITE, (sx, sy), (ex, ey), 6)

                if keys[pygame.K_SPACE] or mouse_down_btn:
                    self.current_phase = GamePhases.SHOOT

            # Skott
            if self.current_phase == GamePhases.SHOOT:
                if self.projectile is None:
                    self.projectile = active_tank.shoot()

            # Projektiluppdatering
            if self.projectile:
                self.projectile.update(dt)
                target = self.right_tank if self.current_player == 1 else self.left_tank
                if target.rect.collidepoint(self.projectile.x, self.projectile.y):
                    target.take_damage(active_tank.damage)
                    self.explosions_active.append(explosions.Explosion(self.projectile.x, self.projectile.y))
                    self.projectile = None
                    self.current_phase = GamePhases.MOVE
                    self.__end_turn()
                elif self.projectile.is_offscreen(self.screen_width, self.screen_height):
                    self.projectile = None
                    self.current_phase = GamePhases.MOVE
                    self.__end_turn()

            # Text - anvisning
            if self.current_phase == GamePhases.MOVE:
                self.info_text.set_text(f"Spelare {self.current_player}: Flytta, sikta och tryck SPACE för att skjuta")

            # Rita allt
            self.left_tank.draw(self.screen)
            self.right_tank.draw(self.screen)

            if self.projectile:
                self.projectile.draw(self.screen)

            for ex in self.explosions_active:
                ex.update(dt)
                ex.draw(self.screen)
                if ex.finished:
                    self.explosions_active.remove(ex)

            # Runda & bränsle‐info
            Text(f"Runda: {self.round_counter}",  None, 30, BLACK, SCREEN_WIDTH-150, 20).draw(self.screen)
            Text(f"Bränsle P1: {int(self.left_tank.fuel)}",  None, 24, BLACK, 20, 50).draw(self.screen)
            Text(f"Bränsle P2: {int(self.right_tank.fuel)}", None, 24, BLACK, SCREEN_WIDTH-160, 50).draw(self.screen)

            self.info_text.draw(self.screen)
            pygame.display.flip()

            if self.left_tank.is_dead() or self.right_tank.is_dead():
                running = False

        # Slutscen & spara 'recent winner'
        winner_name = "Spelare " + str(self.current_player)
        winner_tank = self.right_tank.name if self.left_tank.is_dead() else self.left_tank.name
        country = "USA" if self.right_tank.is_dead() else "Ryssland"
        recent_winner.save_recent_winner(winner_name, winner_tank, country)

        # Visa vinnarmeddelande
        msg = Text(f"{winner_tank} / {winner_name} vann!", None, 60, BLACK, 500, self.screen_height//2-30)
        self.screen.fill(WHITE)
        msg.draw(self.screen)
        pygame.display.flip()
        self.battle_sound.fadeout(4000)
        pygame.time.wait(4000)
