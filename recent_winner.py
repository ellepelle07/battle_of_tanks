import json
import pygame
import gui

# Initiera Pygame
pygame.init()

# Skärmstorlek
SCREEN_WIDTH  = 1450
SCREEN_HEIGHT = 700

BLACK = (0, 0, 0)

# Filväg för att lagra de senaste vinnarna
RECENT_WINNERS_FILE = 'recent_winners.json'

# Bakgrundsbilden för senaste vinnaren
# Se till att pygame.display.set_mode(...) har körts innan denna load
recent_winner_image = pygame.image.load("assets/images/background.jpg")
recent_winner_image = pygame.transform.scale(recent_winner_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


def save_recent_winner(winner_name, tank, country):
    """
    Sparar en vinnare i JSON-filen med de senaste vinnarna.
    Filen måste existera och innehålla giltig JSON-data.
    """
    with open(RECENT_WINNERS_FILE, 'r') as file:
        recent_winners = json.load(file)

    recent_winners.append({
        'name': winner_name,
        'tank': tank,
        'country': country
    })
    recent_winners = recent_winners[-6:][::-1]

    with open(RECENT_WINNERS_FILE, 'w') as file:
        json.dump(recent_winners, file, indent=4)


def get_recent_winners():
    """
    Hämtar de senaste vinnarna från JSON-filen.
    """
    with open(RECENT_WINNERS_FILE, 'r') as file:
        return json.load(file)


def show_winner(screen):
    """
    Visar de senaste vinnarna på en egen skärm.
    Använder den globala recent_winner_image-loadd bilden.
    """
    title_text = gui.Text("Senaste Vinnare", None, 70, BLACK, 250, 50)

    winners = get_recent_winners()
    y_offset = 150
    winner_texts = []

    print(winners)
#    for i, w in enumerate(winners):
 #       text = f"{i+1}. {w['name']} – {w['tank']} {w['country']}"
  #      winner_texts.append(gui.Text(text, None, 30, BLACK, 100, y_offset))
   #     y_offset += 40

    back_text = gui.Text("Tryck ESC för att gå tillbaka", None, 25, BLACK, 100, y_offset + 30)

    running = True
    while running:
        screen.blit(recent_winner_image, (0, 0))
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
                    running = False


if __name__ == "__main__":
    import main
    main.start_game()
