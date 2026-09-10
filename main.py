import pygame

pygame.init()
screen=pygame.display.set_mode((400,300))

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255,255,255))
    pygame.display.update()
