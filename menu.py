import pygame
import gui

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)

# Bakgrundsbilden för menyn
war_image = None

# Initiera Pygame:s mixer för ljudhantering
pygame.mixer.init()

# Ladda ljudfilen för klick
click_sound = pygame.mixer.Sound("assets/sound/click_sound.wav")


def init_menu(screen_width, screen_height):
    global war_image
    # Ladda och skalera menyns bakgrundsbild
    war_image = pygame.image.load("assets/images/war_background.jpg")
    war_image = pygame.transform.scale(war_image, (screen_width, screen_height))


def main_menu(screen):
    button_font = pygame.font.Font(None, 35)
    title_text = gui.Text("Battle of Tanks", "assets/fonts/gomarice_monkey_Area.ttf", 80, BLACK, 250, 100)

    # Instruktionstexter
    instructions = [
        gui.Text("Instruktioner:", None, 30, WHITE, 20, 520),
        gui.Text("1. Använd piltangenter för att röra dig", None, 25, WHITE, 20, 550),
        gui.Text("2. Tryck på SPACE för att skjuta", None, 25, WHITE, 20, 590),
        gui.Text("Tryck 'L' för mer information om spelet", None, 25, WHITE, 20, 640),
    ]

    # Skapa knappar – notera att knappen för "Senaste Vinnare" nu bara skickar en signal
    buttons = [
        gui.Button("Välj Stridsvagn", 300, 240, 200, 50, button_font),
        gui.Button("Senaste Vinnare", 300, 310, 200, 50, button_font),
    ]

    menu_running = True
    while menu_running:
        # Rita bakgrundsbilden
        screen.blit(war_image, (0, 0))
        title_text.draw(screen)

        # Rita instruktionstexterna
        for text in instructions:
            text.draw(screen)

        # Hantera knappmarkering baserat på musposition
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            is_selected = button.rect.collidepoint(mouse_pos)
            button.draw(screen, is_selected)

        pygame.display.flip()

        # Händelsehantering
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        click_sound.play()
                        if button.text == "Välj Stridsvagn":
                            return "select_tank"
                        elif button.text == "Senaste Vinnare":
                            return "show_recent_winner"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    return "instructions"

    return "quit"
