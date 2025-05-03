import json
import pygame
import gui
from shared.constants import *

# Filväg för att lagra de senaste vinnarna
RECENT_WINNERS_FILE = 'recent_winners.json'

# Bakgrundsbilden för senaste vinnaren
# Se till att pygame.display.set_mode(...) har körts innan denna load
recent_winner_image = pygame.image.load("assets/images/background.jpg")
recent_winner_image = pygame.transform.scale(recent_winner_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


def save_recent_winner(winner_name, tank, country):
    """
    Sparar en vinnare i JSON-filen för senaste vinnare.

    Läser in befintliga data, lägger till en ny post och skriver tillbaka
    max sex senaste poster till filen.

    :param winner_name: Namnet på vinnaren, t.ex. 'Spelare 1'.
    :param tank:        Namnet på stridsvagnen som användes.
    :param country:     Landet/världsidan, t.ex. 'USA' eller 'Ryssland'.
    """
    recent_winners = get_recent_winners()
    recent_winners.append({
        'name': winner_name,
        'tank': tank,
        'country': country
    })
    recent_winners = recent_winners[-6:]

    with open(RECENT_WINNERS_FILE, 'w') as file:
        json.dump(recent_winners, file, indent=4)


def get_recent_winners():
    """
    Hämtar en lista med de senaste vinnarna från JSON-filen.

    :return: Lista av dict-objekt med nycklarna 'name', 'tank' och 'country'.
             Returnerar en tom lista om filen inte finns eller innehåller ogiltig JSON.
    """
    try:
        with open(RECENT_WINNERS_FILE, 'r') as file:
            winners = json.load(file)
            return winners
    except:
        return []

def show_winner(screen):
    """
    Visar en skärm med de senaste vinnarna.

    Renderar bakgrundsbild, titel och upp till sex senaste vinnare.
    Väntar på att användaren trycker på ESC för att återgå.

    :param screen: pygame.Surface där skärmen ritas.
    """
    title_text = gui.Text("Senaste Vinnare", None, 70, BLACK, 250, 50)

    winners = get_recent_winners()[::-1]  # Vänd/reversa listan innan den visas på skärmen
    y_offset = 150
    winner_texts = []

    for i, w in enumerate(winners):
        text = f"{i+1}. {w['name']} – {w['country']} - {w['tank']} "
        winner_texts.append(gui.Text(text, None, 30, BLACK, 100, y_offset))
        y_offset += 40

    back_text = gui.Text("Tryck 'ESC' för att gå tillbaka till menyn.", None, 25, BLACK, 100, y_offset + 30)

    running = True
    while running:
        screen.blit(recent_winner_image, (0, 0))
        title_text.draw_text(screen)

        for txt in winner_texts:
            txt.draw_text(screen)
        back_text.draw_text(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
