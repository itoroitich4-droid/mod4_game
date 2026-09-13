import pygame
from utils.authentication import login, register, get_user
from pygame_ui.menu import menu


def login_screen(screen):
    font = pygame.font.Font(None, 45)
    small = pygame.font.Font(None, 28)

    username = ""
    message = ""

    running = True
    image = pygame.image.load("assets/images/back1.jpeg")
    image = pygame.transform.scale(image, (800, 700))

    while running:
        screen.fill((35, 35, 55))
        screen.blit(image, (0, 0))

        title = font.render("101 GAME", True, "white")
        screen.blit(title, (320, 100))

        text = small.render("Username: " + username, True, "white")
        screen.blit(text, (250, 220))

        screen.blit(
            small.render("ENTER = Login", True, "white"),
            (250, 300)
        )

        screen.blit(
            small.render("R = Register", True, "white"),
            (250, 340)
        )

        screen.blit(
            small.render(message, True, "yellow"),
            (250, 400)
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.key == pygame.K_RETURN:

                    if login(username):
                        user = get_user(username)
                        menu(screen, user)
                        return

                    message = "User not found. Press R to register."

                elif event.key == pygame.K_r:

                    if username == "":
                        message = "Type a username first."
                    elif register(username):
                        message = "Registered! Press ENTER."
                    else:
                        message = "Username already exists."

                elif event.key == pygame.K_ESCAPE:
                    return

                else:
                    if len(event.unicode) == 1:
                        username += event.unicode