import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        # Ladda och skala projektilbilden
        self.image = pygame.image.load("assets/sprites/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        g = 300  # pixels/s^2      # GRAVIATION
        self.x += self.vx * dt                       # Horisontell förflyttning
        self.y += self.vy * dt + 0.5 * g * dt * dt   # Kinematikformeln: Vertikal förflyttning med konstant acceleration
        self.vy += g * dt                            # Gravitationspåverkan på den vertikala hastigheten

        # Konvertera flyttal till heltal eftersom pygame.Rect kräver heltalskoordinater
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self, screen_width, screen_height):
        return (self.x < 0 or self.x > screen_width
                or self.y < 0 or self.y > screen_height)

