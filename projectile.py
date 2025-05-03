import pygame

class Projectile(pygame.sprite.Sprite):
    """
    En projektil som färdas med initial hastighet
    och påverkas av gravitation.

    Uppdaterar position och hastighet, ritar sig själv och kan
    kontrollera om den lämnat skärmen.
    """
    def __init__(self, x, y, vx, vy):
        """
        Initierar projektilen med dess startposition och hastighet.

        :param x:  Startkoordinat på x-axeln (i pixlar).
        :param y:  Startkoordinat på y-axeln (i pixlar).
        :param vx: Initial hastighet i x-led (pixlar/sekund).
        :param vy: Initial hastighet i y-led (pixlar/sekund).
        """
        super().__init__()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        # Ladda och skala projektilbilden
        self.image = pygame.image.load("assets/sprites/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=(x, y))

    def update_projectile(self, dt):
        """
        Uppdaterar projektilens fysik och position baserat på delta time.

        Använder kinematiska rörelseekvationer med en konstant gravitationsacceleration.
        :param dt: Tidsdifferens sedan senaste uppdatering (sekunder).
        """
# https://www.kaggle.com/code/dawith/python-for-kinematics-motion-diagram
        g = 300  # pixels/s^2      # GRAVIATION
        self.x += self.vx * dt                       # Horisontell förflyttning
        self.y += self.vy * dt + 0.5 * g * dt * dt   # Kinematikformeln: Vertikal förflyttning med konstant acceleration
        self.vy += g * dt                            # Gravitationspåverkan på den vertikala hastigheten

        # Konvertera flyttal till heltal då pygame.Rect kräver heltalskoordinater
        self.rect.center = (int(self.x), int(self.y))

    def draw_projectile(self, screen):
        """
        Ritar projektilen på den givna ytan.

        :param screen: pygame.Surface där projektilen ska ritas.
        """
        screen.blit(self.image, self.rect)

    def is_off_screen(self, screen_width, screen_height):
        """
        Kontrollerar om projektilen har lämnat skärmområdet.

        :param screen_width:  Bredden på skärmen (pixlar).
        :param screen_height: Höjden på skärmen (pixlar).
        :return:              True om projektilens centrum är utanför skärmen, annars False.
        """
        return (self.x < 0 or self.x > screen_width
                or self.y < 0 or self.y > screen_height)
