import pygame
import math

class Tank(pygame.sprite.Sprite):
    def __init__(self, name, max_hp, damage, x, y, image_path, facing=1, max_fuel=100):
        super().__init__()
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.damage = damage
        self.x = x
        self.y = y
        self.facing = facing
        self.angle = 45 if self.facing == 1 else 135
        # Ladda och skala tankbilden
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (120, 70))
        self.rect = self.image.get_rect(center=(x, y))
        # Projektilhastighet
        self.projectile_speed = 550
        # Bränsleattribut
        self.max_fuel = max_fuel
        self.fuel = max_fuel
        self.fuel_consumption_per_move = 0.45  # förbrukning per förflyttningsanrop

    def move(self, dx):
        """Flytta endast om bränsle finns kvar."""
        if self.fuel >= self.fuel_consumption_per_move:
            self.x += dx
            self.rect.centerx = self.x
            self.fuel -= self.fuel_consumption_per_move
            if self.fuel < 0:
                self.fuel = 0

    def aim(self, da):
        """Justera siktvinkeln inom giltiga intervall."""
        self.angle += da
        if self.facing == 1:
            self.angle = max(0, min(90, self.angle))
        else:
            self.angle = max(90, min(180, self.angle))

    def shoot(self):
        """Skapa och returnera en projektil baserat på nuvarande vinkel."""
        rad = math.radians(self.angle)
        start_x, start_y = self.rect.center
        vx = self.projectile_speed * math.cos(rad)
        vy = -self.projectile_speed * math.sin(rad)
        return Projectile(start_x, start_y, vx, vy)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_dead(self):
        return self.hp == 0

    def draw(self, screen):
        """Rita tanken samt dess HP- och bränsleindikatorer."""
        screen.blit(self.image, self.rect.topleft)
        self.draw_hp_bar(screen)
        self.draw_fuel_bar(screen)

    def draw_hp_bar(self, screen):
        bar_width = 100
        bar_height = 8
        x = self.rect.x
        y = self.rect.y - 20
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        fill_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (x, y, fill_width, bar_height))

    def draw_fuel_bar(self, screen):
        bar_width = 50
        bar_height = 8
        x = self.rect.x
        y = self.rect.y - 10
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        fill_width = int((self.fuel / self.max_fuel) * bar_width)
        pygame.draw.rect(screen, (255, 165, 0), (x, y, fill_width, bar_height))


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
        g = 300  # pixels/s^2
        self.x += self.vx * dt
        self.y += self.vy * dt + 0.5 * g * dt * dt
        self.vy += g * dt
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_offscreen(self, screen_width, screen_height):
        return (self.x < 0 or self.x > screen_width
                or self.y < 0 or self.y > screen_height)
