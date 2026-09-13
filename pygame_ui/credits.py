import pygame

def credits_screen(screen):
    font = pygame.font.Font(None, 35)
    title_font = pygame.font.Font(None, 50)

    while True:
        screen.fill((45, 30, 30))

        title = title_font.render("Credits",True,"yellow")

        screen.blit(title, (320, 70))

        lines = ["101 Game","","Game Developers:","Samuel Omari",
            "Isaac Obuba","Ian Toroitich"]

        for i, text in enumerate(lines):
            image = font.render(text,True,"white")

            screen.blit(image,(250, 140 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return