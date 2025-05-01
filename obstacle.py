import pygame

class Obstacle:
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def collides_with(self, sprite_rect):
        return self.rect.colliderect(sprite_rect)

