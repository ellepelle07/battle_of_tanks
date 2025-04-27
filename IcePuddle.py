import pygame

class IcePuddle:
    def __init__(self, pos):
        self.image = pygame.image.load("assets/sprites/ice_frames.png")
        self.image = pygame.transform.scale(self.image, (600, 150))  # Hårdkodad storlek
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def collides_with(self, sprite_rect):
        return self.rect.colliderect(sprite_rect)

