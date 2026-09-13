import pygame

from models.game import Game
from game.quickplay import get_quickplay_questions
from pygame_ui.results import results


def game_screen(screen, questions=None):

    if questions is None:
        questions = get_quickplay_questions()

    game = Game(questions)

    font = pygame.font.Font(None, 30)
    big_font = pygame.font.Font(None, 42)

    while game.current < len(game.questions):

        question = game.questions[game.current]

        screen.fill((45, 45, 45))

        title = big_font.render(
            "Find the Lie!",
            True,
            "yellow"
        )

        screen.blit(title, (300, 30))

        category = font.render(
            question.category,
            True,
            "cyan"
        )

        screen.blit(category, (30, 90))

        number = font.render(
            f"Question {game.current + 1}/{len(game.questions)}",
            True,
            "white"
        )

        screen.blit(number, (30, 125))

        for i, statement in enumerate(question.statements):

            text = font.render(
                f"{i + 1}. {statement}",
                True,
                "white"
            )

            screen.blit(
                text,
                (40, 190 + i * 70)
            )

        instruction = font.render(
            "Press 1, 2 or 3",
            True,
            "yellow"
        )

        screen.blit(instruction, (320, 420))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3
                ]:

                    answer = event.key - pygame.K_1

                    game.check_answer(answer)

                    game.current += 1

                    break

                if event.key == pygame.K_ESCAPE:
                    return

    results(
        screen,
        game.score,
        len(game.questions)
    )