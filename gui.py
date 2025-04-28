import pygame
from shared.constants import *

class Button:
    """ Representerar en knapp i spelet som man kan interagera med"""
    def __init__(self, text, x, y, width, height, font):
        """
        :param text:    Texten som visas på knappen
        :param x:       X-koordinaten för knappens övre vänstra hörn
        :param y:       X-koordinaten för knappens övre vänstra hörn
        :param width:   Knappens bredd i pixlar
        :param height:  Knappens bredd i pixlar
        :param font:    Typsnittet som används för knapptexten
        """
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font

    def draw(self, screen, is_selected):
        """ Ritar knappen på den angivna skärmen.
        Knappens färg ändras beroende på om den är vald eller inte.

        :param screen:      Skärmytan som knappen ska ritas på
        :param is_selected: Indikerar om knappen är för närvarande vald (t.ex. av muspekaren)
        """
        color = GREEN if is_selected else GRAY

        # Rita knappens rect. vilken skärm, färg, strolek och kant radie?
        pygame.draw.rect(screen, color, self.rect, border_radius=15)

        # Fyll textruta (font) med text
        text_surface = self.font.render(self.text, True, WHITE)

        # Ge texten en rektangel för underlättad positionering
        text_rect = text_surface.get_rect(center=self.rect.center) # get_rect = En rektangel som skapas exakt runt fonten/texten
        screen.blit(text_surface, text_rect)


class Text:
    """ Representerar en textsträng som kan ritas på skärmen.
    Denna klass hanterar textens innehåll, typsnitt, storlek, färg och position."""

    def __init__(self, text, font_path, font_size, color, x, y):
        """ Initierar en ny textinstans.

        :param text:            Texten som ska visas
        :param font_path:       Sökvägen till typsnittet
        :param font_size:       Textens storlek i punkter
        :param color:           Textens färg
        :param x:               X-koordinaten för textens övre vänstra hörn.
        :param y:               Y-koordinaten för textens övre vänstra hörn.
        """
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
        """
        Uppdaterar den interna ytan som innehåller den renderade texten och dess rektangel.
        Denna metod anropas när texten eller dess egenskaper ändras.
        """
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        """
        Ritar texten på den angivna skärmen.

        :param screen:  Skärmytan som texten ska ritas på.
        """
        screen.blit(self.text_surface, self.rect)

    def set_text(self, new_text):
        """ Ändrar texten som visas och uppdaterar den renderade ytan.

        :param new_text: Den nya texten som ska visas.
        """
        self.text = new_text
        self.update_surface()
