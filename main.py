import pygame
from menu import Menu
from enum import Enum
import tank_selection
import game
import recent_winner
from shared.constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle of Tanks - by Elias El Shobaki - Copyright (C) 2025")

# Initiera menyn (bakgrundsbild)
menu = Menu(screen)

class GameStates(Enum):
    MENU = 1,
    SELECT_TANK = 2,
    RECENT_WINNERS = 3

def start_game():
    running = True
    current_state: GameStates = GameStates.MENU

    while running:
        # Tillstånd
        if current_state == GameStates.MENU:
            menu_action = menu.get_action()
            if menu_action == menu.SELECT_TANK:
                current_state = GameStates.SELECT_TANK
            elif menu_action == menu.SHOW_RECENT_WINNERS:
                current_state = GameStates.RECENT_WINNERS
            elif menu_action == menu.QUIT:
                running = False

        elif current_state == GameStates.SELECT_TANK:
            selected_tanks = tank_selection.select_tank(screen)
            if selected_tanks[0] and selected_tanks[1]:
                game.start_battle(selected_tanks, screen)
                current_state = GameStates.MENU

        elif current_state == GameStates.RECENT_WINNERS:
            recent_winner.show_winner(screen)
            current_state = GameStates.MENU

    pygame.quit()

if __name__ == "__main__":
    start_game()
