import pygame
from pygame_ui.login import login_screen

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("101 Game")

pygame.mixer.music.load("assets/sounds/good.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


login_screen(screen)
pygame.quit()