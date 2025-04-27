import pygame
import gui
from shared.constants import *

# Lokala färger
RED = (255, 0, 0)
BLUE = (30, 20, 135)
HOVER_BORDER = (255, 215, 0)  # Gyllene kant vid hover

# Tankstorlekar
TANK_WIDTH = 300
TANK_HEIGHT = 200

class TankSelection:
    def __init__(self, screen):
        self.choose_your_fighter_sound = pygame.mixer.Sound("assets/sound/choose_your_fighter_sound.wav")
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # Ladda och skala bilder för USA-tankar
        self.usa_tank1_img = pygame.image.load("assets/sprites/M1_ABRAMS.png")
        self.usa_tank1_img = pygame.transform.scale(self.usa_tank1_img, (TANK_WIDTH, TANK_HEIGHT))
        self.usa_tank1_img = pygame.transform.flip(self.usa_tank1_img, True, False)
        self.usa_tank2_img = pygame.image.load("assets/sprites/SHERMAN.png")
        self.usa_tank2_img = pygame.transform.scale(self.usa_tank2_img, (TANK_WIDTH, TANK_HEIGHT))
        self.usa_tank2_img = pygame.transform.flip(self.usa_tank2_img, True, False)

        # Ladda och skala bilder för ryska tankar
        self.russia_tank1_img = pygame.image.load("assets/sprites/T90.png")
        self.russia_tank1_img = pygame.transform.scale(self.russia_tank1_img, (TANK_WIDTH, TANK_HEIGHT))
        self.russia_tank2_img = pygame.image.load("assets/sprites/T34.png")
        self.russia_tank2_img = pygame.transform.scale(self.russia_tank2_img, (TANK_WIDTH, TANK_HEIGHT))

        # Ladda symbolbilder
        self.hp_symbol = pygame.image.load("assets/sprites/hp_symbol.png")
        self.damage_symbol = pygame.image.load("assets/sprites/damage_symbol.png")
        self.fuel_symbol = pygame.image.load("assets/sprites/fuel_symbol.png")

        # Skala symbolerna (exempelvis 50x50 pixlar)
        self.hp_symbol = pygame.transform.scale(self.hp_symbol, (50, 50))
        self.damage_symbol = pygame.transform.scale(self.damage_symbol, (50, 50))
        self.fuel_symbol = pygame.transform.scale(self.fuel_symbol, (50, 50))

        # Beräkna positioner för tankarna
        left_center_x = self.screen_width // 4
        right_center_x = 3 * self.screen_width // 4
        top_y = self.screen_height // 3
        bottom_y = 2 * self.screen_height // 3

        # Placera USA-tankar (spelare 1)
        self.player1_tank1_rect = self.usa_tank1_img.get_rect(center=(left_center_x, top_y))
        self.player1_tank2_rect = self.usa_tank2_img.get_rect(center=(left_center_x, bottom_y))
        # Placera ryska tankar (spelare 2)
        self.player2_tank1_rect = self.russia_tank1_img.get_rect(center=(right_center_x, top_y))
        self.player2_tank2_rect = self.russia_tank2_img.get_rect(center=(right_center_x, bottom_y))

        # Skapa textobjekt
        self.title_text = gui.Text("Välj stridsvagn", None, 50, WHITE, self.screen_width // 2 - 150, 50)
        self.usa_label = gui.Text("USA", None, 40, WHITE, self.screen_width // 4 - 30, 50)
        self.soviet_label = gui.Text("Ryssland", None, 40, WHITE, 3 * self.screen_width // 4 - 50, 50)
        self.tank1_title_usa = gui.Text("M1 Abrams", None, 30, WHITE, left_center_x - 50, top_y + TANK_HEIGHT // 2 + 10)
        self.tank2_title_usa = gui.Text("Sherman M4A3E8", None, 30, WHITE, left_center_x - 50, bottom_y + TANK_HEIGHT // 2 + 10)
        self.tank1_title_soviet = gui.Text("T-90", None, 30, WHITE, right_center_x - 50, top_y + TANK_HEIGHT // 2 + 10)
        self.tank2_title_soviet = gui.Text("T-34", None, 30, WHITE, right_center_x - 50, bottom_y + TANK_HEIGHT // 2 + 10)

        self.choose_your_fighter_sound.play()

        self.selection = [None, None]

    def draw(self):
        # Rita bakgrunder: vänster halva blå, höger halva röd
        self.screen.fill(BLUE, rect=pygame.Rect(0, 0, self.screen_width // 2, self.screen_height))
        self.screen.fill(RED, rect=pygame.Rect(self.screen_width // 2, 0, self.screen_width // 2, self.screen_height))

        # Rita texter
        self.usa_label.draw(self.screen)
        self.soviet_label.draw(self.screen)
        self.title_text.draw(self.screen)

        # Rita stridsvagnarna
        self.screen.blit(self.usa_tank1_img, self.player1_tank1_rect)
        self.screen.blit(self.usa_tank2_img, self.player1_tank2_rect)
        self.screen.blit(self.russia_tank1_img, self.player2_tank1_rect)
        self.screen.blit(self.russia_tank2_img, self.player2_tank2_rect)

        # Rita tanktitlar
        self.tank1_title_usa.draw(self.screen)
        self.tank2_title_usa.draw(self.screen)
        self.tank1_title_soviet.draw(self.screen)
        self.tank2_title_soviet.draw(self.screen)

        # Rita symboler:
        # De övre tankarna får hp_symbol i övre vänstra hörnet
        hp_rect1 = self.hp_symbol.get_rect(topleft=self.player1_tank1_rect.topleft)
        hp_rect2 = self.hp_symbol.get_rect(topleft=self.player2_tank1_rect.topleft)
        self.screen.blit(self.hp_symbol, hp_rect1)
        self.screen.blit(self.hp_symbol, hp_rect2)

        # De övre tankarna får även fuel_symbol i övre högra hörnet
        fuel_rect1 = self.fuel_symbol.get_rect(topright=self.player1_tank1_rect.topleft)
        fuel_rect2 = self.fuel_symbol.get_rect(topright=self.player2_tank1_rect.topleft)
        self.screen.blit(self.fuel_symbol, fuel_rect1)
        self.screen.blit(self.fuel_symbol, fuel_rect2)

        # De nedre tankarna får damage_symbol i övre vänstra hörnet
        dmg_rect1 = self.damage_symbol.get_rect(topleft=self.player1_tank2_rect.topleft)
        dmg_rect2 = self.damage_symbol.get_rect(topleft=self.player2_tank2_rect.topleft)
        self.screen.blit(self.damage_symbol, dmg_rect1)
        self.screen.blit(self.damage_symbol, dmg_rect2)

        # Rita markeringsramar vid hover
        mouse_pos = pygame.mouse.get_pos()
        if self.player1_tank1_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, HOVER_BORDER, self.player1_tank1_rect, 4)
        if self.player1_tank2_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, HOVER_BORDER, self.player1_tank2_rect, 4)
        if self.player2_tank1_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, HOVER_BORDER, self.player2_tank1_rect, 4)
        if self.player2_tank2_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, HOVER_BORDER, self.player2_tank2_rect, 4)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if pos[0] < self.screen_width // 2:
                if self.player1_tank1_rect.collidepoint(pos):
                    self.selection[0] = "M1 Abrams"
                elif self.player1_tank2_rect.collidepoint(pos):
                    self.selection[0] = "Sherman M4A3E8"
            else:
                if self.player2_tank1_rect.collidepoint(pos):
                    self.selection[1] = "T-90"
                elif self.player2_tank2_rect.collidepoint(pos):
                    self.selection[1] = "T-34"
        return self.selection

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                else:
                    self.handle_event(event)
            if self.selection[0] and self.selection[1]:
                running = False
            clock.tick(60)
        return self.selection

def select_tank(screen):
    ts = TankSelection(screen)
    return ts.run()
