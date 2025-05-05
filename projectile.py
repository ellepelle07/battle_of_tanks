import pygame

class Projectile(pygame.sprite.Sprite):
    """
    En projektil som färdas med initial hastighet
    och påverkas av gravitation.

    Uppdaterar position och hastighet, ritar sig själv och kan
    kontrollera om den lämnat skärmen.
    """
    def __init__(self, start_x, start_y, vx, vy):
        """
        Initierar projektilen med dess startposition och hastighet.

        :param start_x:  Startkoordinat på x-axeln (i pixlar).
        :param start_y:  Startkoordinat på y-axeln (i pixlar).
        :param vx: Initial hastighet i x-led (pixlar/sekund).
        :param vy: Initial hastighet i y-led (pixlar/sekund).
        """
        super().__init__()
        self.x = start_x
        self.y = start_y
        self.vx = vx
        self.vy = vy
        # Ladda och skala projektilbilden
        self.image = pygame.image.load("assets/sprites/bullet.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=(start_x, start_y))

    def update_projectile(self, dt):
        """
        Uppdaterar projektilens fysik och position baserat på delta time.

        Använder kinematiska rörelseekvationer med en konstant gravitationsacceleration.
        :param dt: Tidsdifferens sedan senaste uppdatering (sekunder).
        """
# https://www.kaggle.com/code/dawith/python-for-kinematics-motion-diagram
        g = 300  # pixels/s^2       Gravitationsaccelerationen
        self.x += self.vx * dt                       # Horisontell förflyttning
        self.y += self.vy * dt + 0.5 * g * dt * dt   # Kinematikformeln: Beräknar vilken y position skottet baserat på tid(dt), acceleration(g) och begynnelsehastigheten i y-led(vy)
        self.vy += g * dt                            # Gravitationspåverkan på den vertikala hastigheten

        # Konvertera flyttal till heltal då pygame.Rect kräver heltalskoordinater
        self.rect.center = (self.x, self.y)

    def draw_projectile(self, screen):
        """
        Ritar projektilen på den givna ytan.

        :param screen: pygame.Surface där projektilen ska ritas.
        """
        screen.blit(self.image, self.rect)
