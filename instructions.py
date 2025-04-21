import pygame
import gui

GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

profile_picture = pygame.image.load("assets/images/profile_picture.jpg")
profile_picture = pygame.transform.scale(profile_picture, (198, 300))

def draw_instructions(screen, SCREEN_WIDTH):
    screen.fill(GRAY)

    # Rita profilbild och text
    screen.blit(profile_picture, (SCREEN_WIDTH - 400, 15))
    gui.Text("CREDIT: Elias El Shobaki", None, 30, BLACK, SCREEN_WIDTH - 400, 320).draw(screen)
    gui.Text("Programmering 1", None, 30, BLACK, SCREEN_WIDTH - 400, 360).draw(screen)
    gui.Text("2025", None, 30, BLACK, SCREEN_WIDTH - 400, 390).draw(screen)

    instructions = [
        gui.Text("Om spelet:", "assets/fonts/gomarice_kamone_6.ttf", 40, BLACK, 20, 20),
        gui.Text("Battle of Tanks (BoT) är ett 1v1-spel där två spelare möts på slagfältet", None, 30, BLACK, 20, 70),
        gui.Text("i varsin stridsvagn. Spelarna får turas om med att förflytta, sikta och skjuta", None, 30, BLACK, 20, 110),
        gui.Text("mot motståndarens stridsvagn. Varje stridsvagn har sina egna egenskaper – vissa är ", None, 30, BLACK, 20, 150),
        gui.Text("tåliga med mycket HP, andra är mer explosiva men med begränsat bränsle.", None, 30, BLACK, 20, 190),

        gui.Text("Varje runda börjar med att spelaren får flytta sin tank, men varje rörelse kostar bränsle,", None, 30, BLACK, 20, 260),
        gui.Text("så det gäller att tänka taktiskt. Därefter siktar man med musen och skjuter.", None, 30, BLACK, 20, 300),

        gui.Text("Målet är simpelt: Var den sista stridsvagnen som rullar.", None, 30,BLACK, 20, 370),

        gui.Text("Tryck 'M' för att gå tillbaka till menyn.", None, 30, BLACK, 20, 450),
    ]
    for text in instructions:
        text.draw(screen)

    pygame.display.flip()

