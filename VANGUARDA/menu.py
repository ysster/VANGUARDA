import pygame
import sys

from cutscene import Cutscene
from jogo_principal import Jogo


class Menu:
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.largura = largura
        self.altura = altura

        # FUNDO
        self.fundo = pygame.image.load("assets/Fundo.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))

        # LOGO
        self.logo = pygame.image.load("assets/Vanguarda.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (600, 200))
        self.logo_rect = self.logo.get_rect(center=(largura // 2, 160))

        # BOTÕES
        self.btn_play = pygame.image.load("assets/buttons/START.png").convert_alpha()
        self.btn_options = pygame.image.load("assets/buttons/SETTINGS.png").convert_alpha()
        self.btn_exit = pygame.image.load("assets/buttons/EXIT.png").convert_alpha()

        self.btn_play = pygame.transform.scale(self.btn_play, (125, 60))
        self.btn_options = pygame.transform.scale(self.btn_options, (150, 60))
        self.btn_exit = pygame.transform.scale(self.btn_exit, (115, 60))

        self.btn_play_rect = self.btn_play.get_rect(center=(largura // 2, 300))
        self.btn_options_rect = self.btn_options.get_rect(center=(largura // 2, 380))
        self.btn_exit_rect = self.btn_exit.get_rect(center=(largura // 2, 460))

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.logo, self.logo_rect)
        self.tela.blit(self.btn_play, self.btn_play_rect)
        self.tela.blit(self.btn_options, self.btn_options_rect)
        self.tela.blit(self.btn_exit, self.btn_exit_rect)

    def executar(self):
        clock = pygame.time.Clock()
        rodando = True

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # PLAY
                    if self.btn_play_rect.collidepoint(evento.pos):
                        rodando = False  # fecha menu

                        # CUTSCENE
                        cutscene = Cutscene(self.tela, self.largura, self.altura)
                        cutscene.executar()

                        # JOGO
                        jogo = Jogo()
                        jogo.executar()

                    # OPTIONS (ainda vazio)
                    if self.btn_options_rect.collidepoint(evento.pos):
                        print("OPTIONS")

                    # EXIT
                    if self.btn_exit_rect.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()

            self.desenhar()
            pygame.display.update()
            clock.tick(60)
