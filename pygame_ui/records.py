import pygame
from utils.file_handler import read_json


def records_screen(screen):

    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 50)

    data = read_json("data/users.json")

    users = data["users"]

    users.sort(
        key=lambda user: user["score"],
        reverse=True
    )

    while True:

        screen.fill((35, 35, 50))

        title = title_font.render("STREAK RECORDS ",True,"yellow")

        screen.blit(title, (270, 50))

        for i, user in enumerate(users):

            text = font.render(f"{i + 1}. {user['username']} - {user['score']}",True,"white")

            screen.blit(text,(270, 130 + i * 45))

        instruction = font.render("Press ESC to return",True,"white")

        screen.blit(instruction,(280, 500) )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return