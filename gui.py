import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)

class Button:
    def __init__(self, text, x, y, width, height, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font

    def draw(self, screen, is_selected):
        color = GREEN if is_selected else GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Text:
    def __init__(self, text, font_path, font_size, color, x, y):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font_path, font_size)
        self.update_surface()

    def update_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def set_text(self, new_text):
        self.text = new_text
        self.update_surface()

    def set_color(self, new_color):
        self.color = new_color
        self.update_surface()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_surface()

    def set_font_size(self, new_size):
        self.font_size = new_size
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.update_surface()
