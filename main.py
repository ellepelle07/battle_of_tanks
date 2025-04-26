import pygame
from menu import Menu
import tank_selection
import game
import recent_winner

pygame.init()

SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle of Tanks - by Elias El Shobaki - Copyright (C) 2025")

# Ladda profilbild
profile_picture = pygame.image.load("assets/images/profile_picture.jpg")
profile_picture = pygame.transform.scale(profile_picture, (198, 300))

# Initiera menyn (bakgrundsbild)
menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

def start_game():
    running = True
    current_state = "menu"

    while running:
        # Tillstånd
        if current_state == "menu":
            menu_action = menu.get_action()
            if menu_action == "select_tank":
                current_state = "select_tank"
            elif menu_action == "show_recent_winner":
                current_state = "show_recent_winner"
            elif menu_action == "quit":
                running = False

        elif current_state == "select_tank":
            selected_tanks = tank_selection.select_tank(screen)
            if selected_tanks[0] and selected_tanks[1]:
                game.start_battle(selected_tanks, screen)
                current_state = "menu"

        elif current_state == "show_recent_winner":
            recent_winner.show_winner(screen)
            current_state = "menu"

    pygame.quit()

if __name__ == "__main__":
    start_game()
