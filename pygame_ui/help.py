import pygame


def help_screen(screen):

    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 45)

    while True:

        screen.fill((30, 30, 50))

        title = title_font.render(
            "How To Play",
            True,
            "yellow"
        )

        screen.blit(title, (300, 50))

        instructions = [
            "There are three statements.",
            "Two  are true.",
            "One  is not true.",
            "Choose the number of the lie.",
            "",
            "   1 = First statement",
            "   2 = Second statement",
            "   3 = Third statement",
            "",
            "Press ESC to go back."
        ]

        for i, text in enumerate(instructions):

            image = font.render(
                text,
                True,
                "white"
            )

            screen.blit(
                image,
                (180, 120 + i * 40)
            )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return