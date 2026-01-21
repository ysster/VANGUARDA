import pygame
from menu import Menu

pygame.init()

LARGURA = 1200
ALTURA = 800

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("VANGUARDA")

menu = Menu(tela, LARGURA, ALTURA)
menu.executar()
