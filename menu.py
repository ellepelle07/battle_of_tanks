import time
import pygame
import gui

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)

# Initiera Pygame:s mixer för ljudhantering
pygame.mixer.init()

# Ladda ljudfilen för klick
click_sound = pygame.mixer.Sound("assets/sound/click_sound.wav")

class Menu:
    # Bakgrundsbilden för menyn
    war_image = None
    screen_width = None

    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        # Ladda och skala menyns bakgrundsbild
        self.war_image = pygame.image.load("assets/images/war_background.jpg")
        self.war_image = pygame.transform.scale(self.war_image, (screen_width, screen_height))
        self.screen_width = screen_width

    # Privat metod som bara får användas i denna klass
    def __show_menu(self):
        # Rita bakgrundsbilden
        self.screen.blit(self.war_image, (0, 0))
        title_text = gui.Text("Battle of Tanks", "assets/fonts/gomarice_monkey_Area.ttf", 80, BLACK, 250, 100)
        title_text.draw(self.screen)
        button_font = pygame.font.Font(None, 35)

        # Instruktionstexter
        instructions_text = [
            gui.Text("Instruktioner:", None, 30, WHITE, 20, 520),
            gui.Text("1. Använd piltangenter för att röra dig", None, 25, WHITE, 20, 550),
            gui.Text("2. Tryck på SPACE för att skjuta", None, 25, WHITE, 20, 590),
            gui.Text("Tryck 'H' för mer information om spelet", None, 25, WHITE, 20, 640),
        ]

        # Rita instruktionstexterna
        for text in instructions_text:
            text.draw(self.screen)

        # Skapa knappar – notera att knappen för "Senaste Vinnare" nu bara skickar en signal
        self.buttons = [
            gui.Button("Välj Stridsvagn", 300, 240, 200, 50, button_font),
            gui.Button("Senaste Vinnare", 300, 310, 200, 50, button_font),
        ]

        pygame.display.flip()

    def __show_instructions(self):
        self.screen.fill(GRAY)
        profile_picture = pygame.image.load("assets/images/profile_picture.jpg")
        profile_picture = pygame.transform.scale(profile_picture, (198, 300))
        # Rita profilbild och text
        self.screen.blit(profile_picture, (self.screen_width - 400, 15))
        gui.Text("CREDIT: Elias El Shobaki", None, 30, BLACK, self.screen_width - 400, 320).draw(self.screen)
        gui.Text("Programmering 1", None, 30, BLACK, self.screen_width - 400, 360).draw(self.screen)
        gui.Text("2025", None, 30, BLACK, self.screen_width - 400, 390).draw(self.screen)

        instructions_text = [
            gui.Text("Om spelet:", "assets/fonts/gomarice_kamone_6.ttf", 40, BLACK, 20, 20),
            gui.Text("Battle of Tanks (BoT) är ett 1v1-spel där två spelare möts på slagfältet", None, 30, BLACK, 20,
                     70),
            gui.Text("i varsin stridsvagn. Spelarna får turas om med att förflytta, sikta och skjuta", None, 30, BLACK,
                     20, 110),
            gui.Text("mot motståndarens stridsvagn. Varje stridsvagn har sina egna egenskaper – vissa är ", None, 30,
                     BLACK, 20, 150),
            gui.Text("tåliga med mycket HP, andra är mer explosiva men med begränsat bränsle.", None, 30, BLACK, 20,
                     190),

            gui.Text("Varje runda börjar med att spelaren får flytta sin tank, men varje rörelse kostar bränsle,", None,
                     30, BLACK, 20, 260),
            gui.Text("så det gäller att tänka taktiskt. Därefter siktar man med musen och skjuter.", None, 30, BLACK,
                     20, 300),

            gui.Text("Målet är simpelt: Var den sista stridsvagnen som rullar.", None, 30, BLACK, 20, 370),

            gui.Text("Tryck 'ESC' för att gå tillbaka till menyn.", None, 30, BLACK, 20, 450),
        ]
        for text in instructions_text:
            text.draw(self.screen)

        pygame.display.flip()

    def get_action(self):
        clock = pygame.time.Clock()
        instruction_enabled = False
        self.__show_menu()
        while True:
            if not instruction_enabled:
                # Hantera knappmarkering baserat på musposition
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    is_selected = button.rect.collidepoint(mouse_pos)
                    button.draw(self.screen, is_selected)
                pygame.display.flip()

            # Hantera tangenttryck
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            click_sound.play()
                            if button.text == "Välj Stridsvagn":
                                return "select_tank"
                            elif button.text == "Senaste Vinnare":
                                return "show_recent_winner"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        instruction_enabled = True
                        self.__show_instructions()

                    if event.key == pygame.K_ESCAPE:
                        self.__show_menu()

            clock.tick(25)
