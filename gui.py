import pygame
from shared.constants import *

class Button:
    def __init__(self, text, x, y, width, height, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font

    def draw(self, screen, is_selected):
        color = GREEN if is_selected else GRAY

        # Rita knappens rect. vilken skärm, färg, strolek och kant radie?
        pygame.draw.rect(screen, color, self.rect, border_radius=15)

        # Fyll textruta (font) med text
        text_surface = self.font.render(self.text, True, WHITE)

        # Ge texten en rektangel för underlättad positionering
        text_rect = text_surface.get_rect(center=self.rect.center) # get_rect = En rektangel som skapas exakt runt fonten/texten
        screen.blit(text_surface, text_rect)


class Text:
    def __init__(self, text, font_path, font_size, color, x, y):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        self.x = x
        self.y = y
        self.text_surface = None
        self.rect = None
        self.font = pygame.font.Font(font_path, font_size)
        self.update_surface()

    def update_surface(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.text_surface, self.rect)

    def set_text(self, new_text):
        self.text = new_text
        self.update_surface()
