import pygame


def results(screen, score, total):

    font = pygame.font.Font(None, 45)
    small = pygame.font.Font(None, 30)

    while True:

        screen.fill((55, 40, 55))

        title = font.render(
            "Game Over!",
            True,
            "white"
        )

        screen.blit(title, (300, 150))

        score_text = small.render(
            f"Score: {score}/{total}",
            True,
            "yellow"
        )

        screen.blit(score_text, (330, 230))

        text = small.render(
            "Press ENTER to return",
            True,
            "white"
        )

        screen.blit(text, (280, 320))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return