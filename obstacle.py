
class Obstacle:
    """
    Representerar ett hinder i spelvärlden.

    Objektet har en bild och en rektangel för kollision och rendering.
    """
    def __init__(self, image, pos):
        """
        Skapar ett nytt hinder vid given position.

        :param image: pygame.Surface som representerar hinderets grafik.
        :param pos:   Tuple (x, y) som anger centrumposition i pixlar.
        """
        self.image = image
        self.rect = self.image.get_rect(center=pos)

    def draw_obstacle(self, surface):
        """
        Renderar hindret på den angivna ytan.

        :param surface: pygame.Surface där hindret ska ritas.
        """
        surface.blit(self.image, self.rect.topleft)

    def collides_with(self, sprite_rect):
        """
        Kontrollerar om hindret kolliderar med en given sprite-rektangel.

        :param sprite_rect: pygame.Rect för den kolliderande sprite:n.
        :return:            True om rektanglarna överlappar, annars False.
        """
        return self.rect.colliderect(sprite_rect)

