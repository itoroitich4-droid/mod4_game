import pygame

from pygame_ui.game_screen import game_screen
from pygame_ui.category_screen import category_screen
from pygame_ui.daily_challenge_screen import daily_challenge_screen
from pygame_ui.help import help_screen
from pygame_ui.credits import credits_screen
from pygame_ui.records import records_screen


def menu(screen, user):

    font = pygame.font.Font(None, 50)
    small = pygame.font.Font(None, 30)
    background = pygame.image.load("assets/images/main2.jpeg")
    background = pygame.transform.scale(background, (800, 600))

    while True:

        screen.fill((35, 35, 55))
        screen.blit(background, (0, 0))

        title = font.render("101 GAME", True, "white")
        screen.blit(title, (310, 50))

        welcome = small.render(
            "Welcome " + user["username"],
            True,
            "yellow"
        )

        screen.blit(welcome, (330, 110))

        buttons = [
            "1. Quickplay",
            "2. Categories",
            "3. Streak Challenge",
            "4. Help",
            "5. Credits",
            "6. Records",
            "7. Exit"
        ]

        for i, text in enumerate(buttons):

            image = small.render(text, True, "white")

            screen.blit(
                image,
                (300, 160 + i * 45)
            )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    game_screen(screen)

                elif event.key == pygame.K_2:
                    category_screen(screen)

                elif event.key == pygame.K_3:
                    daily_challenge_screen(screen,user)

                elif event.key == pygame.K_4:
                    help_screen(screen)

                elif event.key == pygame.K_5:
                    credits_screen(screen)

                elif event.key == pygame.K_6:
                    records_screen(screen)

                elif event.key == pygame.K_7:
                    return