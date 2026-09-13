import pygame

from game.daily_challenge import get_daily_questions
from utils.authentication import update_score


def daily_challenge_screen(screen,user):

    questions = get_daily_questions()

    font = pygame.font.Font(None, 35)
    title_font = pygame.font.Font(None, 45)

    score = 0
    current = 0

    while current < len(questions):

        question = questions[current]

        screen.fill((50, 40, 20))

        title = title_font.render(
            "Streak Challenge",
            True,
            "yellow"
        )

        screen.blit(title, (280, 40))

        streak = font.render(
            f"Current Streak: {score}",
            True,
            "white"
        )

        screen.blit(streak, (300, 100))

        for i, statement in enumerate(question.statements):

            text = font.render(
                f"{i + 1}. {statement}",
                True,
                "white"
            )

            screen.blit(
                text,
                (50, 180 + i * 80)
            )

        instruction = font.render(
            "Choose the lie: 1, 2 or 3",
            True,
            "yellow"
        )

        screen.blit(instruction, (250, 430))

        pygame.display.flip()

        answered = False

        while not answered:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return

                    if event.key in [
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3
                    ]:

                        answer = event.key - pygame.K_1

                        if answer == question.answer:
                            score += 1
                            current += 1
                            answered = True

                        else:
                            answered = True
                            update_score(user["username"], score)

                            screen.fill((50, 20, 20))

                            game_over = title_font.render(
                                "Streak Over!",
                                True,
                                "red"
                            )

                            screen.blit(
                                game_over,
                                (300, 180)
                            )

                            result = font.render(
                                f"Final Streak: {score}",
                                True,
                                "white"
                            )

                            screen.blit(
                                result,
                                (300, 250)
                            )

                            text = font.render(
                                "Press ENTER to return",
                                True,
                                "white"
                            )

                            screen.blit(
                                text,
                                (250, 330)
                            )

                            pygame.display.flip()

                            waiting = True

                            while waiting:

                                for event in pygame.event.get():

                                    if event.type == pygame.QUIT:
                                        return

                                    if event.type == pygame.KEYDOWN:

                                        if event.key == pygame.K_RETURN:
                                            return

                                        if event.key == pygame.K_ESCAPE:
                                            return

    # Player answered all questions correctly

    screen.fill((20, 50, 30))

    title = title_font.render(
        "Amazing!",
        True,
        "yellow"
    )

    screen.blit(title, (320, 180))

    result = font.render(
        f"Final Streak: {score}",
        True,
        "white"
    )

    screen.blit(result, (300, 250))

    text = font.render(
        "Press ENTER to return",
        True,
        "white"
    )

    screen.blit(text, (250, 330))

    pygame.display.flip()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return

                if event.key == pygame.K_ESCAPE:
                    return