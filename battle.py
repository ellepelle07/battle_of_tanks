import time
import pygame
import sys
import math
from gui import Text
from tank import Tank
import recent_winner
import explosions
from enum import Enum
from shared.constants import *
from obstacle import Obstacle
from random import randint

# Inställningar
AIM_LINE_LENGTH = 320
GROUND_LEVEL = SCREEN_HEIGHT - 92
FUEL_BONUS_PER_ROUND = 15    # Bränslebonus varje hel runda
TARGET_AREA_COLOR = (255, 0, 0)


# Ladda bakgrundsbild
background_image = pygame.image.load("assets/images/battlefield_background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

T90_IMG = "assets/sprites/T90.png"
T34_IMG = "assets/sprites/T34.png"
M1_ABRAMS_IMG = "assets/sprites/M1_ABRAMS.png"
SHERMAN_IMG =  "assets/sprites/SHERMAN.png"

class GamePhases(Enum):
    """
    Enum som representerar de olika faserna i spelet:
    """

    MOVE = 1,
    AIM = 2,
    SHOOT = 3


def draw_dashed_line(screen, color, start_pos, end_pos, dash_length=10):
    """
    Ritar en streckad linje mellan två punkter på given skärm.

    :param screen:      pygame.Surface där linjen ska ritas.
    :param color:       Färg på linjen som en RGB-tuple, t.ex. (255, 0, 0).
    :param start_pos:   Startkoordinat som tuple (x, y).
    :param end_pos:     Slutkoordinat som tuple (x, y).
    :param dash_length: Längd på varje streck i pixlar (standard=10).
    """

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
        pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 3)


class Battle:
    """
    Hanterar hela spelomgången.
    """

    def __init__(self, screen, selected_tanks):
        """
        Initierar Battle-objektet med resurser, ljud, hinder och spelparametrar.

        :param screen:          pygame.Surface som används för rendering.
        :param selected_tanks:  Lista med två strängar från tank_selection.py, valda tanknamn för spelare 1 och 2.
        """

        self.screen = screen
        self.battle_sound = pygame.mixer.Sound("assets/sound/battle_sound.ogg")
        self.engine_sound = pygame.mixer.Sound("assets/sound/engine_sound.mp3")
        puddle = pygame.image.load("assets/sprites/ice_frames.png")
        self.puddle_img = pygame.transform.scale(puddle, (600, 150))  # Hårdkodad storlek
        self.engine_playing = False
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = screen.get_size()
        self.puddle = Obstacle(self.puddle_img,(self.screen_width // 2, GROUND_LEVEL))
        self.current_phase: GamePhases = GamePhases.MOVE
        self.current_player = randint(1, 2)  # Slumpa vilken spelar som börjar
        self.projectile = None
        self.explosions_active = []
        self.round_counter = 1
        self.turns_in_round = 0
        self.info_text = Text("", None, 30, BLACK, 50, 20)
        self.left_tank  = self.__create_tank(selected_tanks[0], 100, GROUND_LEVEL, facing=1)
        self.right_tank = self.__create_tank(selected_tanks[1], self.screen_width-200, GROUND_LEVEL, facing=-1)

    def __explode_projectile(self):
        """
        Lägger till en explosion på projektilens plats, tar bort projektilen,
        byter till nästa spelare och återgår till flyttfasen.
        """
        self.explosions_active.append(explosions.Explosion(self.projectile.x, self.projectile.y))
        self.projectile = None
        self.current_phase = GamePhases.MOVE
        self.__end_turn()

    def __create_tank(self, name, x, bottom_y, facing):
        """
        Skapar och returnerar en Tank-instans baserat på namnet.

        :param name:     Sträng med tankens namn, t.ex. "M1 Abrams" eller "T-90".
        :param x:        X-koordinat för tankens mitt.
        :param bottom_y: Y-koordinat för tankens botten (marknivå).
        :param facing:   Riktning tanken vänder: 1 = höger, -1 = vänster.
        :return:         Ett Tank-objekt med korrekt HP, skada och bränsle.
        """

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
        t = Tank(
            name=name,
            max_hp=hp,
            damage=dmg,
            x=x, y=bottom_y,
            image_path=img,
            screen_width=self.screen_width,
            facing=facing,
            max_fuel=fuel

        )
        t.rect.bottom = bottom_y
        t.x = t.rect.centerx
        return t

    def __end_turn(self):
        """
        Växlar aktuell spelare, räknar turer per runda och tilldelar
        bränslebonus om båda spelare spelat en tur.
        """
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
        """
        Startar spelets huvudloop
        """
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
                self.info_text.set_text(f"Spelare {self.current_player}: Flytta, sikta och tryck SPACE för att skjuta")
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

                # Aim  >>>>>>KOLLA OM MAN KAN INTEGRERA DENNA MED aim-metoden i tank.py<<<<<<<<<
                # Exempel: i Battle.start() hantera tryck på ↑/↓
                # if keys[pygame.K_UP]:
                #     active_tank.aim(+1)
                # if keys[pygame.K_DOWN]:
                #     active_tank.aim(-1)

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
                draw_dashed_line(self.screen, WHITE, (sx, sy), (ex, ey), 10)

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
                    self.__explode_projectile()
                elif self.projectile.is_off_screen(self.screen_width, self.screen_height):
                    self.__explode_projectile()
                elif self.projectile.y > GROUND_LEVEL:
                    self.__explode_projectile()

            # Rita allt
            self.left_tank.draw(self.screen)
            self.right_tank.draw(self.screen)

            if self.projectile:
                self.projectile.draw(self.screen)

            for ex in self.explosions_active:
                ex.update(dt)
                ex.draw(self.screen)  # Anropar dynamiskt Projectile-klassens draw-metod
                if ex.finished:
                    self.explosions_active.remove(ex)

            # Runda & bränsle‐info
            Text(f"Runda: {self.round_counter}",  None, 40, BLACK, SCREEN_WIDTH // 2 - 60, 20).draw(self.screen)
            Text(f"Bränsle USA: {int(self.left_tank.fuel)}",  None, 24, BLACK, 20, 50).draw(self.screen)
            Text(f"Bränsle Ryssland: {int(self.right_tank.fuel)}", None, 24, BLACK, SCREEN_WIDTH-190, 50).draw(self.screen)

            self.info_text.draw(self.screen)
            pygame.display.flip()

            if self.left_tank.is_dead() or self.right_tank.is_dead():
                time.sleep(0.6)
                running = False

        # Slutscen & spara 'recent winner'
        winner_player = 1 if self.current_player == 2 else 2
        winner_name = "Spelare " + str(winner_player)
        winner_tank = self.left_tank.name if winner_player == 1 else self.right_tank.name
        country = "USA" if winner_player == 1 else "Ryssland"
        recent_winner.save_recent_winner(winner_name, winner_tank, country)

        # Visa vinnarmeddelande
        msg = Text(f"{winner_tank} / {winner_name} vann!", None, 60, BLACK, 500, self.screen_height//2-30)
        self.screen.fill(WHITE)
        msg.draw(self.screen)
        pygame.display.flip()
        self.battle_sound.fadeout(4000)
        pygame.time.wait(4000)
