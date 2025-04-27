import pygame

# Flagga för att kontrollera om resurserna är laddade
resources_loaded = False
explosion_images = []
explosion_sound: pygame.mixer.Sound

def load_explosion_resources():
    global explosion_images, explosion_sound, resources_loaded
    if not resources_loaded:
        explosion_images = [
            pygame.image.load("assets/sprites/explosion_1.png").convert_alpha(),
            pygame.image.load("assets/sprites/explosion_2.png").convert_alpha(),
            pygame.image.load("assets/sprites/explosion_3.png").convert_alpha(),
            pygame.image.load("assets/sprites/explosion_4.png").convert_alpha()
        ]
        explosion_sound = pygame.mixer.Sound("assets/sound/explosion.wav")
        resources_loaded = True


class Explosion:
    def __init__(self, x, y):
        load_explosion_resources()  # Säkerställ att resurser laddas först
        self.images = explosion_images
        self.x = x
        self.y = y
        self.frame = 0
        self.timer = 0
        self.finished = False
        play_explosion_sound()

    def update(self, dt):
        self.timer += dt
        if self.timer >= 0.1:
            self.timer = 0
            self.frame += 1
            if self.frame >= len(self.images):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            image = self.images[self.frame]
            screen.blit(image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))


def play_explosion_sound():
    if explosion_sound:
        explosion_sound.play()
