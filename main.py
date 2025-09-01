import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("DakFarm 2009")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((100, 200, 100))
    text = font.render("Welcome to DakFarm 2009 (Demo)", True, (255, 255, 255))
    screen.blit(text, (200, 250))

    pygame.display.update()
    clock.tick(60)
