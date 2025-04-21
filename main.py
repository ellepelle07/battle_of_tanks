import pygame
import sys
import menu
import tank_selection
import game
import instructions

pygame.init()

SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle of Tanks - Elias El Shobaki")

# Ladda profilbild
profile_picture = pygame.image.load("assets/images/profile_picture.jpg")
profile_picture = pygame.transform.scale(profile_picture, (198, 300))

# Initiera menyn (bakgrundsbild)
menu.init_menu(SCREEN_WIDTH, SCREEN_HEIGHT)

def start_game():
    running = True
    current_state = "menu"
    clock = pygame.time.Clock()

    while running:
        # Hantera globala quit- och navigationstangenter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l and current_state == "menu":
                    current_state = "instructions"
                elif event.key == pygame.K_m and current_state == "instructions":
                    current_state = "menu"

        # Tillstånd
        if current_state == "menu":
            action = menu.main_menu(screen)
            if action == "select_tank":
                current_state = "select_tank"
            elif action == "instructions":
                current_state = "instructions"
            elif action == "show_recent_winner":
                current_state = "show_recent_winner"
            elif action == "quit":
                running = False

        elif current_state == "select_tank":
            selected_tanks = tank_selection.select_tank(screen)
            if selected_tanks[0] and selected_tanks[1]:
                game.start_battle(selected_tanks, screen)
                current_state = "menu"

        elif current_state == "instructions":
            instructions.draw_instructions(screen, SCREEN_WIDTH)

        elif current_state == "show_recent_winner":
            menu.show_winner(screen)
            current_state = "menu"

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_game()
