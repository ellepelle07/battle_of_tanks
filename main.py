import pygame
from menu import Menu
from enum import Enum
from tank_selection import TankSelection
from battle import Battle
import recent_winner
from shared.constants import *


pygame.init()

# Initiera Pygame:s mixer för ljudhantering
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle of Tanks - by Elias El Shobaki - Copyright (C) 2025")

# Initiera menyn (bakgrundsbild)
menu = Menu(screen)


class GameStates(Enum):
    """
    De olika tillstånden som spelet kan befinna sig i.
    Varje tillstånd har ett unikt värde som identifierar den aktuella fasen av spelet.
    """

    MENU = 1,
    SELECT_TANK = 2,
    RECENT_WINNERS = 3

def start_game():
    """
    Startar spelet och hanterar spelets huvudloop samt de olika tillstånden.
    Spelet initieras i menytillståndet och fortsätter sedan baserat på användarens interaktioner.
    """

    running = True
    current_state: GameStates = GameStates.MENU

    while running:
        # Hanterar de olika tillstånden
        if current_state == GameStates.MENU:
            menu_action = menu.get_action()
            if menu_action == menu.SELECT_TANK:
                current_state = GameStates.SELECT_TANK
            elif menu_action == menu.SHOW_RECENT_WINNERS:
                current_state = GameStates.RECENT_WINNERS
            elif menu_action == menu.QUIT:
                running = False

        elif current_state == GameStates.SELECT_TANK:
            ts = TankSelection(screen)
            selected_tanks = ts.run()
            if selected_tanks[0] and selected_tanks[1]:
                Battle(screen, selected_tanks)
                current_state = GameStates.MENU

        elif current_state == GameStates.RECENT_WINNERS:
            recent_winner.show_winner(screen)
            current_state = GameStates.MENU

    pygame.quit()


if __name__ == "__main__":
    start_game()
