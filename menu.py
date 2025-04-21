import pygame
import gui
import recent_winner      # Importera recent_winner-modulen

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY  = (150, 150, 150)

war_image          = None
recent_winner_image = None

# Initiera Pygame:s mixer för ljudhantering
pygame.mixer.init()

# Ladda ljudfilen
click_sound = pygame.mixer.Sound("assets/sound/click_sound.wav")


def init_menu(screen_width, screen_height):
    global war_image, recent_winner_image
    war_image = pygame.image.load("assets/images/war_background.jpg")
    war_image = pygame.transform.scale(war_image, (screen_width, screen_height))

    recent_winner_image = pygame.image.load("assets/images/background.jpg")
    recent_winner_image = pygame.transform.scale(recent_winner_image, (screen_width, screen_height))


def main_menu(screen):
    button_font = pygame.font.Font(None, 35)
    title_text = gui.Text("Battle of Tanks", "assets/fonts/gomarice_monkey_Area.ttf", 80, BLACK, 250, 100)

    instructions = [
        gui.Text("Instruktioner:", None, 30, WHITE, 20, 520),
        gui.Text("1. Använd piltangenter för att röra dig", None, 25, WHITE, 20, 550),
        gui.Text("2. Tryck på SPACE för att skjuta", None, 25, WHITE, 20, 590),
        gui.Text("Tryck 'L' för mer information om spelet", None, 25, WHITE, 20, 640),
    ]

    buttons = [
        gui.Button("Välj Stridsvagn", 300, 240, 200, 50, button_font),
        gui.Button("Senaste Vinnare", 300, 310, 200, 50, button_font),
    ]

    menu_running = True
    while menu_running:
        screen.blit(war_image, (0, 0))
        title_text.draw(screen)

        for text in instructions:
            text.draw(screen)

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            is_selected = button.rect.collidepoint(mouse_pos)
            button.draw(screen, is_selected)

        pygame.display.flip()

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


def show_winner(screen):
    """Visar de senaste vinnarna med bakgrundsbild."""
    global recent_winner_image


    title_text = gui.Text("Senaste Vinnare", None, 70, BLACK, 250, 50)

    winners = recent_winner.get_recent_winners()
    winner_texts = []
    y_offset = 150
    for i, w in enumerate(winners):
        tank    = w.get('tank',    'Okänd tank')
        country = w.get('country', 'Okänt land')
        winner_texts.append(
            gui.Text(f"{i+1}. {w['name']} – {tank} ({country})", None, 30, BLACK, 100, y_offset)
        )
        y_offset += 40

    back_text = gui.Text("Tryck ESC för att gå tillbaka", None, 25, BLACK, 100, y_offset + 30)

    waiting = True
    while waiting:
        if recent_winner_image:
            screen.blit(recent_winner_image, (0, 0))
        else:
            screen.fill(WHITE)

        title_text.draw(screen)
        for txt in winner_texts:
            txt.draw(screen)
        back_text.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False


if __name__ == "__main__":
    import main
    main.start_game()
