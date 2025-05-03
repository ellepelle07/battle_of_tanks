import pygame

#Modul för explosionseffekter i spelet.


resources_loaded = False
explosion_images = []
explosion_sound: pygame.mixer.Sound

def load_explosion_resources():
    """
    Laddar explosioners bilder och ljud om de inte redan är laddade.
    Använder globala variabler:
      - explosion_images: Lista med för bilder.
      - explosion_sound: pygame.mixer.Sound för explosionseffekten.
      - resources_loaded: Bool som indikerar om resurserna redan laddats.
    """
    global explosion_images, explosion_sound, resources_loaded
    if not resources_loaded:
        # convert_alpha() - Ladda bilderna, konvertera dem för snabbare rendering och behåll transparens (alfa-kanal)
        explosion_images = [
            pygame.image.load("assets/sprites/explosion_1.png").convert_alpha(),
            pygame.image.load("assets/sprites/explosion_2.png").convert_alpha(),
            pygame.image.load("assets/sprites/explosion_3.png").convert_alpha(),
            pygame.image.load("assets/sprites/explosion_4.png").convert_alpha()
        ]
        explosion_sound = pygame.mixer.Sound("assets/sound/explosion.wav")
        resources_loaded = True


class Explosion:
    """
    Representerar en explosion i spelet.

    Hanterar animering av explosionsbilder, uppspelning av ljud
    och säger till när animationen är klar.
    """
    def __init__(self, x, y):
        """
        Skapar en explosionsinstans på given skärposition.

        :param x: X-koordinat för explosionens centrum.
        :param y: Y-koordinat för explosionens centrum.
        """
        load_explosion_resources()  # Säkerställ att resurser laddas först
        self.images = explosion_images
        self.x = x
        self.y = y
        self.frame = 0
        self.timer = 0
        self.finished = False
        explosion_sound.play()

    def update_explosions(self, dt):
        """
        Uppdaterar explosionens animeringsstatus baserat på tid.

        Använder en intern timer för att byta bildramar med jämna intervall.
        :param dt: Delta time är den tid (i sekunder) sedan senaste uppdatering.
                   Används för att se till att explosionens animation gäller samma takt
                   oavsett spelets bildfrekvens (FPS)
        """

        self.timer += dt
        if self.timer >= 0.1:
            self.timer = 0
            self.frame += 1
            if self.frame >= len(self.images):
                self.finished = True

    def draw_explosions(self, screen):
        """
        Renderar aktuell explosionsbild på given skärm.

        :param screen: pygame.Surface där explosionen ritas.
        """
        if not self.finished:
            image = self.images[self.frame]
            screen.blit(image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))

