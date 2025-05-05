import pygame

#Modul för explosionseffekter i spelet.


resources_loaded = False
explosion_images = []
explosion_sound: pygame.mixer.Sound

# Lägger inte detta i initieringen eftersom det tar tid att ladda bilder från mina filer och det skapas nya explotioner hela tiden.
# Man vill inte behöva ladda in bilder varje gång. Därför vill man tima denna funktion så att den inte stör spelet.
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
        # kan lägga till convert_alpha() - Ladda bilderna, konvertera dem för snabbare rendering och behåll transparens (alfa-kanal)
        explosion_images = [
            pygame.image.load("assets/sprites/explosion_1.png"),
            pygame.image.load("assets/sprites/explosion_2.png"),
            pygame.image.load("assets/sprites/explosion_3.png"),
            pygame.image.load("assets/sprites/explosion_4.png")
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
        self.rect = None
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
        if self.timer >= 0.15:  # Hur länge varje bild ska vara på skärmen
            self.timer = 0
            self.frame += 1     # Frame = vilken bild den är på
            if self.frame >= len(self.images):
                self.finished = True

    def draw_explosions(self, screen):
        """
        Renderar aktuell explosionsbild på given skärm.

        :param screen: pygame.Surface där explosionen ritas.
        """
        if not self.finished:
            image = self.images[self.frame] # Väljer vild fråm images baserat på vilken frame vi är på
            self.rect = image.get_rect(center=(self.x, self.y))
            screen.blit(image, self.rect)
