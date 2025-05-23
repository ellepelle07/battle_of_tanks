import pygame
import gui
from shared.constants import *

class Menu:
    """
    Klass som hanterar spelets huvudmeny, inklusive visning av instruktioner och användarinteraktion.
    """
    # Konstanter
    SELECT_TANK = 1
    SHOW_RECENT_WINNERS = 2
    QUIT = 3

    def __init__(self, screen):
        """
        Initierar Menu-objektet med nödvändiga resurser som bilder och ljud.

        :param screen: Pygame-yta där menyn ska ritas.
        """
        self.screen = screen
        # Ladda och skala menyns bakgrundsbild
        self.war_image = pygame.image.load("assets/images/war_background.jpg")
        self.war_image = pygame.transform.scale(self.war_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Ladda ljudfiler
        self.menu_sound = pygame.mixer.Sound("assets/sound/menu_sound.mp3")
        self.click_sound = pygame.mixer.Sound("assets/sound/click_sound.wav")

        # Skapa en dedikerad kanal för menyljudet, så att vi inte spelar upp flera instanser samtidigt
        self.menu_channel = pygame.mixer.Channel(1)

    # Privat metod som bara får användas i denna klass
    def __show_menu(self):
        """
        Privat metod som ritar huvudmenyn och dess knappar samt visar instruktionstexter.
        """
        # Rita bakgrundsbilden
        self.screen.blit(self.war_image, (0, 0))
        title_text = gui.Text("Battle of Tanks", "assets/fonts/gomarice_monkey_Area.ttf", 80, BLACK, 250, 100)
        title_text.draw_text(self.screen)

        # Instruktionstexter
        instructions_text = [
            gui.Text("Instruktioner:", None, 30, WHITE, 20, 520),
            gui.Text("1. Använd piltangenter för att styra", None, 25, WHITE, 20, 550),
            gui.Text("2. Tryck på SPACE för att skjuta", None, 25, WHITE, 20, 590),
            gui.Text("Tryck 'H' för mer information om spelet", None, 25, WHITE, 20, 640),
        ]

        # Rita instruktionstexterna
        for text in instructions_text:
            text.draw_text(self.screen)

        # Skapa knappar – notera att knappen för "Senaste Vinnare" nu bara skickar en signal
        self.buttons = [
            gui.Button("Välj Stridsvagn", 300, 240, 200, 50, None, 35),
            gui.Button("Senaste Vinnare", 300, 310, 200, 50, None, 35),
        ]

        pygame.display.flip()

    def __show_instructions(self):
        """
        Privat metod som visar spelets instruktioner och bakgrundsinformation.
        """
        self.screen.fill(GRAY)
        profile_picture = pygame.image.load("assets/images/profile_picture.jpg")
        profile_picture = pygame.transform.scale(profile_picture, (198, 300))
        # Rita profilbild och text
        self.screen.blit(profile_picture, (SCREEN_WIDTH - 400, 15))
        gui.Text("CREDIT: Elias El Shobaki", None, 30, BLACK, SCREEN_WIDTH - 400, 320).draw_text(self.screen)
        gui.Text("Programmering 1", None, 30, BLACK, SCREEN_WIDTH - 400, 360).draw_text(self.screen)
        gui.Text("2025", None, 30, BLACK, SCREEN_WIDTH - 400, 390).draw_text(self.screen)
        gui.Text("Betyg:  A?", None, 30,BLACK, SCREEN_WIDTH - 400, 430 ).draw_text(self.screen)

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
            text.draw_text(self.screen)

        pygame.display.flip()

    def get_action(self):
        """
        Visar menyn, hanterar användarinmatning och returnerar användarens val.

        :return: Ett heltal som representerar användarens menyval:
                 SELECT_TANK, SHOW_RECENT_WINNERS eller QUIT.
        """
        clock = pygame.time.Clock()
        instruction_enabled = False
        self.__show_menu()
        # Spela menyljudet på den dedikerade kanalen endast om det inte redan spelar
        if not self.menu_channel.get_busy():
            self.menu_channel.play(self.menu_sound, loops=-1)
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
                    return self.QUIT

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            self.click_sound.play()
                            if button.text == "Välj Stridsvagn":
                                self.menu_channel.fadeout(2000)
                                return self.SELECT_TANK
                            elif button.text == "Senaste Vinnare":
                                return self.SHOW_RECENT_WINNERS

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        instruction_enabled = True
                        self.__show_instructions()

                    if event.key == pygame.K_ESCAPE and instruction_enabled:
                        instruction_enabled = False
                        self.__show_menu()

            clock.tick(25)
