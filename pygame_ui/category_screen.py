import pygame

from game.categories import (
    get_categories,
    get_category_questions
)

from pygame_ui.game_screen import game_screen


def category_screen(screen):

    categories = get_categories()

    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 45)

    while True:

        screen.fill((30, 50, 45))

        title = title_font.render(
            "Choose a Category",
            True,
            "yellow"
        )

        screen.blit(title, (270, 25))

        for i, category in enumerate(categories):

            text = font.render(f"{i}. {category}",True,"white")

            x = 50 if i < 5 else 420
            y = 100 + (i % 5) * 70

            screen.blit(text, (x, y))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                number = None

                if pygame.K_1 <= event.key <= pygame.K_9:
                    number = event.key - pygame.K_1

                elif event.key == pygame.K_0:
                    number = 9

                if number is not None:

                    if number < len(categories):

                        questions = get_category_questions(
                            categories[number]
                        )

                        game_screen(screen, questions)

                        return

                if event.key == pygame.K_ESCAPE:
                    return