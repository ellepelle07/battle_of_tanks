import pygame
import math
from projectile import Projectile


# Klassen Tank ärver från basklassen pygame.sprite.Sprite
# vilket ger den tillgång till Pygame:s sprite-system
class Tank(pygame.sprite.Sprite):
    """
    Representerar en spelbar stridsvagn.
    """
    def __init__(self, name, max_hp, damage, x, y, image_path, screen_width, facing=1, max_fuel=100):
        """
        Initierar en Tank-instans med alla dess attribut och resurser.

        :param name: Sträng som identifierar tanktypen.
        :param max_hp: Maximal hälsa (HP) för tanken.
        :param damage: Skadevärdet projektilen kommer att åstadkomma.
        :param x: Startpositionens x-koordinat (mitten).
        :param y: Startpositionens y-koordinat (mitten).
        :param image_path: Sökväg till bildfil för tanken.
        :param screen_width: Skärmens bredd används för gränskoll.
        :param facing: Riktning tanken vänder (1=höger, -1=vänster).
        :param max_fuel: Det maximala bränslet en tank kan ha.
        """
        super().__init__()  # Anropar basklassens __init__ för att initiera Sprite-funktionalitet
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.damage = damage
        self.x = x
        self.y = y
        self.facing = facing
        # Standardvinkel beroende på riktning
        self.angle = 45 if self.facing == 1 else 135

        # Ladda och skala tankbilden
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (120, 70))
        self.image = pygame.transform.flip(self.image, facing == 1, False)

        self.screen_width = screen_width
        # Rektangel för kollisions- och positionshantering
        self.rect = self.image.get_rect(center=(x, y))

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
            if 0 <= (self.x + dx) <= self.screen_width:
                self.x += dx
                self.rect.centerx = self.x
            return True  # Rörelse lyckades
        return False  # Ingen rörelse på grund av bränslebrist

    def aim(self, target_x, target_y):
        """
        Siktar på en punkt (t.ex. muspekaren), klipper vinkeln efter facing.

        :param target_x: X-koordinat dit tanken ska sikta (t.ex. musens x).
        :param target_y: Y-koordinat dit tanken ska sikta (t.ex. musens y).
        """
        # Beräkna vektor från tankens centrum till målet
        dx = target_x - self.rect.centerx
        dy = self.rect.centery - target_y

        # Räkna ut rå vinkel i grader
        raw = math.degrees(math.atan2(dy, dx))
        if raw < 0:
            raw += 360

        # Klipp beroende på vilken sida tanken vänder
        if self.facing == 1:
            self.angle = max(0, min(90, int(raw)))
        else:
            self.angle = max(90, min(180, int(raw)))

    def shoot(self):
        """
        Skapar och returnerar en projektil från tankens centrum med riktning och hastighet.

        :return: En Projectile-instans initierad för skjutningen.
        """
        rad = math.radians(self.angle)
        start_x, start_y = self.rect.center
        vx = self.projectile_speed * math.cos(rad)
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

## KAN MAN SKRIVA DETTA PÅ ETT ANNAT SÄTT??
    def is_dead(self):
        """
        Kontrollerar om tankens HP har gått ner till noll.

        :return: True om hp == 0, annars False.
        """
        return self.hp == 0

    def draw(self, screen):
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
        x = self.rect.x
        y = self.rect.y - 20
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        fill_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (x, y, fill_width, bar_height))

    def draw_fuel_bar(self, screen):
        """
        Ritar en bränslebar ovanför tanken baserat på aktuell bränslemängd.

        :param screen: pygame.Surface där bränslebaren ritas.
        """
        bar_width = 50
        bar_height = 8
        x = self.rect.x
        y = self.rect.y - 10
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        fill_width = int((self.fuel / self.max_fuel) * bar_width)
        pygame.draw.rect(screen, (255, 165, 0), (x, y, fill_width, bar_height))
