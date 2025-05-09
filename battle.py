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
import random

# Inställningar
AIM_LINE_LENGTH = 320
GROUND_LEVEL = SCREEN_HEIGHT - 92
FUEL_BONUS_PER_ROUND = 25    # Bränslebonus varje hel runda

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
    SHOOT = 2


def draw_dashed_line(screen, color, start_pos, end_pos, dash_length=10):
    """
    Ritar en streckad linje mellan två punkter på given skärm.

    :param screen:      pygame.Surface där linjen ska ritas.
    :param color:       Färg på linjen som en RGB-tuple, t.ex. (255, 0, 0).
    :param start_pos:   Startkoordinat som tuple (x, y).
    :param end_pos:     Slutkoordinat som tuple (x, y).
    :param dash_length: Önskade längden för varje streck på linjen i pixlar (standard=10).
    """

    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1

    dash_count = AIM_LINE_LENGTH // dash_length

    for i in range(dash_count):
        # Beräkna streckets startpunkt
        start_x = x1 + (dx * i / dash_count)   # dx * 'i / dash_count' är hur långt på vägen strecket har kommit (i procent).
        start_y = y1 + (dy * i / dash_count)
        # Beräkna streckets slutpunkt
        end_x = x1 + (dx * (i + 0.3) / dash_count)  # addera med 0.3 för att skapa mellanrum
        end_y = y1 + (dy * (i + 0.3) / dash_count)
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
        brick_wall = pygame.image.load("assets/images/brick_wall.jpg")

        self.brick_wall_img = pygame.transform.scale(brick_wall, (50, 240))  # Storlek på objektet
        self.engine_playing = False
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = screen.get_size()
        self.brick_wall = Obstacle(self.brick_wall_img,(self.screen_width // 2, GROUND_LEVEL))

        self.current_phase: GamePhases = GamePhases.MOVE
        self.current_player = random.randint(1, 2)  # Slumpa vilken spelar som börjar
        self.projectile = None
        self.explosions_active = []
        self.round_counter = 1
        self.turns_in_round = 0
        self.info_text = Text("", None, 30, BLACK, 50, 20)

        self.left_tank  = self.__create_tank(selected_tanks[0], 100, GROUND_LEVEL, facing=1)
        self.right_tank = self.__create_tank(selected_tanks[1], self.screen_width-100, GROUND_LEVEL, facing=-1)

        # Starta spelet redan vid initieringen
        self.__start()

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
            hp   = 260
            dmg  = 35
            fuel = 500
            img  = M1_ABRAMS_IMG if name == "M1 Abrams" else T90_IMG
        else:
            hp   = 175
            dmg  = 65
            fuel = 210
            img  = SHERMAN_IMG if name.startswith("Sherman") else T34_IMG

        # Skapa tank och ge den max_fuel
        t = Tank(
            name=name,
            max_hp=hp,
            damage=dmg,
            start_x=x, start_bottom_y=bottom_y,
            image_path=img,
            screen_width=self.screen_width,
            facing=facing,
            max_fuel=fuel
        )

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

    def __start(self):
        """
        Startar spelets huvudloop
        """
        self.battle_sound.play(loops=-1)
        running = True
        while running:
            # Ett flyttal som säger hur många sekunder som förflutit sedan förra uppdateringen.
            dt = self.clock.tick(60) / 1000.0

            mouse_down_btn = False
            active_tank = self.left_tank if self.current_player == 1 else self.right_tank
            self.screen.blit(background_image, (0, 0))
            self.brick_wall.draw_obstacle(self.screen)

            # Rita tankarna
            self.left_tank.draw_tank(self.screen)
            self.right_tank.draw_tank(self.screen)


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
                moved = None
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    moved = active_tank.move(-1)
                    if self.brick_wall.rect.colliderect(active_tank.rect):
                        moved = active_tank.move(1)
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    moved = active_tank.move(1)
                    if self.brick_wall.rect.colliderect(active_tank.rect):
                        moved = active_tank.move(-1)

                if moved:  # Om rörelsen lyckades
                    if not self.engine_playing:
                        self.engine_sound.play(loops=-1)  # Starta motorljudet
                        self.engine_playing = True
                else:
                    # Stoppa motorljudet om ingen tangent trycks
                    self.engine_sound.stop()
                    self.engine_playing = False

                # Sikta med mus
                mx, my = pygame.mouse.get_pos()
                active_tank.aim(mx, my)

                # Rita siktlinje
                rad = math.radians(active_tank.angle)
                sx, sy = active_tank.rect.center
                ex = sx + AIM_LINE_LENGTH * math.cos(rad)  # cos och sin ger förskjutningen i x- respektive y-led
                ey = sy - AIM_LINE_LENGTH * math.sin(rad)
                draw_dashed_line(self.screen, WHITE, (sx, sy), (ex, ey), 10)

                if keys[pygame.K_SPACE] or mouse_down_btn:
                    self.current_phase = GamePhases.SHOOT

            # Skott
            if self.current_phase == GamePhases.SHOOT:
                self.engine_sound.stop()
                if self.projectile is None:
                    self.projectile = active_tank.shoot()

            # Projektiluppdatering: om en projektil existererar ska renderingen och fysiken hanteras
            if self.projectile:
                self.projectile.draw_projectile(self.screen)
                self.projectile.update_projectile(dt)
                target = self.right_tank if self.current_player == 1 else self.left_tank
                if target.rect.colliderect(self.projectile.rect):
                        #target.move(-5) if self.current_player == 1 else target.move(5)  <<<för push-back effekt>>>
                    self.__explode_projectile()
                    target.take_damage(active_tank.damage)
                elif self.projectile.x < 0 or self.projectile.x > self.screen_width or self.projectile.y > GROUND_LEVEL or self.projectile.y < 0:
                    self.__explode_projectile()
                elif self.brick_wall.rect.colliderect(self.projectile.rect):
                    self.__explode_projectile()

            # Explosioner
            for ex in self.explosions_active:
                ex.update_explosions(dt)
                ex.draw_explosions(self.screen)
                if ex.finished:
                    self.explosions_active.remove(ex)

            # Runda & bränsle‐info
            Text(f"Runda: {self.round_counter}",  None, 40, BLACK, SCREEN_WIDTH // 2 - 60, 20).draw_text(self.screen)
            Text(f"Bränsle USA: {int(self.left_tank.fuel)}",  None, 24, BLACK, 20, 50).draw_text(self.screen)
            Text(f"Bränsle Ryssland: {int(self.right_tank.fuel)}", None, 24, BLACK, SCREEN_WIDTH-190, 50).draw_text(self.screen)

            self.info_text.draw_text(self.screen)
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
        self.screen.fill(BLUE) if winner_player == 1 else self.screen.fill(RED)
        msg.draw_text(self.screen)
        pygame.display.flip()
        self.battle_sound.fadeout(4000)
        pygame.time.wait(4000)
