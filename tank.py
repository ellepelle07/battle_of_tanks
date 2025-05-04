import pygame
import math
from projectile import Projectile

# Lokala färger
ORANGE = (255, 165, 0)
GRAY_BAR = (50, 50, 50)
GREEN_HEALTH = (0, 255, 0)

# Klassen Tank ärver från basklassen pygame.sprite.Sprite
# vilket ger den tillgång till Pygame:s sprite-system
class Tank(pygame.sprite.Sprite):
    """
    Representerar en spelbar stridsvagn.
    """
    def __init__(self, name, max_hp, damage, start_x, start_bottom_y, image_path, screen_width, facing=1, max_fuel=100):
        """
        Initierar en Tank-instans med alla dess attribut och resurser.

        :param name:            Sträng som identifierar tanktypen.
        :param max_hp:          Maximal hälsa (HP) för tanken.
        :param damage:          Skadevärdet projektilen kommer att åstadkomma.
        :param start_x:         Startpositionens x-koordinat (mitten).
        :param start_bottom_y:  Startpositionens y-koordinat (botten).
        :param image_path:      Sökväg till bildfil för tanken.
        :param screen_width:    Skärmens bredd används för gränskoll.
        :param facing:          Riktning tanken vänder (1=höger, -1=vänster).
        :param max_fuel:        Det maximala bränslet en tank kan ha.
        """
        super().__init__()  # Anropar basklassens __init__ för att initiera Sprite-funktionalitet
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.damage = damage
        self.facing = facing
        # Standardvinkel beroende på riktning
        self.angle = None

        # Ladda och skala tankbilden
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (120, 70))
        self.image = pygame.transform.flip(self.image, facing == 1, False)

        self.screen_width = screen_width

        self.rect = self.image.get_rect(centerx= start_x, bottom= start_bottom_y)

        # Projektilhastighet
        self.projectile_speed = 550

        # Bränsleattribut
        self.max_fuel = max_fuel
        self.fuel = max_fuel
        self.fuel_consumption_per_move = 0.45  # förbrukning per förflyttningsanrop

    def move(self, dx):
        """
        Flytta endast om bränsle finns kvar.

        :param dx: Förflyttning i x-led (pixlar).
        """
        if self.fuel >= self.fuel_consumption_per_move:
            self.fuel -= self.fuel_consumption_per_move
            if self.fuel < 0:
                self.fuel = 0
            if 0 <= (self.rect.centerx + dx) <= self.screen_width:
                self.rect.centerx += dx

            return True  # Rörelse lyckades
        return False  # Ingen rörelse på grund av bränslebrist

    def aim(self, mx, my):
        """
        Siktar på en punkt (t.ex. muspekaren), klipper vinkeln efter facing.

        :param mx: X-koordinat dit tanken ska sikta (musens x).
        :param my: Y-koordinat dit tanken ska sikta (musens y).
        """
        # Beräkna vektor från tankens centrum till målet
        dx = mx - self.rect.centerx  # dx = avståndet från tankens mitt till musen
        dy = self.rect.centery - my

        # Räkna ut rå vinkel i grader     (math.atan2(dy, dx)) är vinkeln i radianer
        raw_degree = math.degrees(math.atan2(dy, dx))

        # Klipp vinkeln efter tankens facing
        if self.facing == 1:
            self.angle = max(0, min(90, int(raw_degree)))
        else:
            self.angle = max(90, min(180, int(raw_degree)))

    def shoot(self):
        """
        Skapar och returnerar en projektil från tankens centrum med riktning och hastighet.

        :return: En Projectile-instans initierad för skjutningen.
        """
        # tar tankens siktvinkel i grader (self.angle) och gör om den till radianer (rad)
        rad = math.radians(self.angle)
        start_x, start_y = self.rect.center
        # Hur snabbt det ska röra sig i sidled
        vx = self.projectile_speed * math.cos(rad)
        # Hur snabbt det ska röra sig upp/ned
        vy = -self.projectile_speed * math.sin(rad)
        return Projectile(start_x, start_y, vx, vy)

    def take_damage(self, amount):
        """
        Minskar tankens HP med angivet skadevärde och ser till att inte gå under noll.

        :param amount: Mängd skada som ska tillämpas.
        """
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_dead(self):
        """
        Kontrollerar om tankens HP har gått ner till noll.

        :return: True om hp == 0, annars False.
        """
        return self.hp == 0

    def draw_tank(self, screen):
        """Renderar tanken och dess status på skärmen - HP och bränsle.

        :param screen: pygame.Surface där tanken ritas."""
        screen.blit(self.image, self.rect.topleft)
        self.draw_hp_bar(screen)
        self.draw_fuel_bar(screen)

    def draw_hp_bar(self, screen):
        """
        Ritar en hälsobar ovanför tanken baserat på aktuell HP.

        :param screen: pygame.Surface där hälsobaren ritas.
        """
        bar_width = 100
        bar_height = 8
        x = self.rect.x  # positionen för rektangelns vänstra kant som omsluter tanken
        y = self.rect.y - 20
        pygame.draw.rect(screen, GRAY_BAR, (x, y, bar_width, bar_height))
        fill_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(screen, GREEN_HEALTH, (x, y, fill_width, bar_height))

    def draw_fuel_bar(self, screen):
        """
        Ritar en bränslebar ovanför tanken baserat på aktuell bränslemängd.

        :param screen: pygame.Surface där bränslebaren ritas.
        """
        bar_width = 50
        bar_height = 8
        x = self.rect.x
        y = self.rect.y - 10
        pygame.draw.rect(screen, GRAY_BAR, (x, y, bar_width, bar_height))
        fill_width = int((self.fuel / self.max_fuel) * bar_width)
        pygame.draw.rect(screen, ORANGE, (x, y, fill_width, bar_height))
