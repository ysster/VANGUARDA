import pygame
import sys
from jogo_principal import Jogo

pygame.init()
pygame.mixer.init()

# ================== SELEÇÃO DE PERSONAGEM ==================
class SelecaoPersonagem:
    def __init__(self, tela, largura, altura, fonte):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.fonte = fonte

        self.BRANCO = (255, 255, 255)
        self.COR_DESTAQUE = (0, 255, 0)
        self.COR_NORMAL = (200, 200, 200)

        # Painel
        largura_painel = 800
        altura_painel = 400
        x = (largura - largura_painel) // 2
        y = (altura - altura_painel) // 2

        self.painel_rect = pygame.Rect(x, y, largura_painel, altura_painel)
        self.bg_painel = pygame.Surface((largura_painel, altura_painel), pygame.SRCALPHA)
        self.bg_painel.fill((0, 0, 0, 120))  # 🔥 transparência ajustada

        self.CHAR_A = "char_a"
        self.CHAR_B = "char_b"

        # 🔥 tamanho maior e igual para ambos
        TAM = 160

        x_centro = x + largura_painel // 2
        dist = 200
        y_chars = y + 210

        # Carregar personagens
        self.img_char1 = pygame.image.load("assets/Escolhamenino.png").convert_alpha()
        self.img_char2 = pygame.image.load("assets/Escolhamenina.png").convert_alpha()

        self.img_char1 = pygame.transform.scale(self.img_char1, (TAM, TAM))
        self.img_char2 = pygame.transform.scale(self.img_char2, (TAM, TAM))

        # 🔥 centralização correta
        self.rect_char1 = self.img_char1.get_rect(center=(x_centro - dist, y_chars))
        self.rect_char2 = self.img_char2.get_rect(center=(x_centro + dist, y_chars))

    def desenhar(self, mouse):
        self.tela.blit(self.bg_painel, self.painel_rect.topleft)

        titulo = self.fonte.render("Escolha seu personagem", True, self.BRANCO)
        self.tela.blit(
            titulo,
            titulo.get_rect(center=(self.largura // 2, self.painel_rect.y + 50))
        )

        # Bordas de seleção
        pygame.draw.rect(
            self.tela,
            self.COR_DESTAQUE if self.rect_char1.collidepoint(mouse) else self.COR_NORMAL,
            self.rect_char1.inflate(12, 12),
            3
        )
        pygame.draw.rect(
            self.tela,
            self.COR_DESTAQUE if self.rect_char2.collidepoint(mouse) else self.COR_NORMAL,
            self.rect_char2.inflate(12, 12),
            3
        )

        # Personagens
        self.tela.blit(self.img_char1, self.rect_char1)
        self.tela.blit(self.img_char2, self.rect_char2)

    def rodar(self, fundo):
        rodando = True
        escolha = None

        while rodando:
            mouse = pygame.mouse.get_pos()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if self.rect_char1.collidepoint(e.pos):
                        escolha = self.CHAR_A
                        rodando = False
                    elif self.rect_char2.collidepoint(e.pos):
                        escolha = self.CHAR_B
                        rodando = False

            self.tela.blit(fundo, (0, 0))
            self.desenhar(mouse)
            pygame.display.flip()

        return escolha


# ================== MENU PRINCIPAL ==================
class Menu:
    def __init__(self):
        self.largura, self.altura = 1400, 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("VANGUARDA")

        self.fundo = pygame.image.load("assets/Fundo.jpg").convert()
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

        self.logo = pygame.image.load("assets/Vanguarda.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (520, 140))
        self.logo_rect = self.logo.get_rect(
            center=(self.largura // 2, self.altura // 2 - 260)
        )

        tamanho_btn = (220, 65)

        self.btn_play = pygame.image.load("assets/buttons/START.png").convert_alpha()
        self.btn_play = pygame.transform.scale(self.btn_play, tamanho_btn)

        self.btn_options = pygame.image.load("assets/buttons/OPTIONS.png").convert_alpha()
        self.btn_options = pygame.transform.scale(self.btn_options, tamanho_btn)

        self.btn_exit = pygame.image.load("assets/buttons/EXIT.png").convert_alpha()
        self.btn_exit = pygame.transform.scale(self.btn_exit, tamanho_btn)

        y_base = self.altura // 2 - 100
        espacamento = 70

        self.play_rect = self.btn_play.get_rect(center=(self.largura // 2, y_base))
        self.options_rect = self.btn_options.get_rect(center=(self.largura // 2, y_base + espacamento))
        self.exit_rect = self.btn_exit.get_rect(center=(self.largura // 2, y_base + espacamento * 2))

        self.selecao = SelecaoPersonagem(
            self.tela,
            self.largura,
            self.altura,
            pygame.font.SysFont(None, 36)
        )

    def rodar(self):
        rodando = True

        while rodando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    rodando = False

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if self.play_rect.collidepoint(e.pos):
                        escolha = self.selecao.rodar(self.fundo)
                        if escolha:
                            Jogo(escolha).executar()

                    elif self.exit_rect.collidepoint(e.pos):
                        rodando = False

            self.tela.blit(self.fundo, (0, 0))
            self.tela.blit(self.logo, self.logo_rect)
            self.tela.blit(self.btn_play, self.play_rect)
            self.tela.blit(self.btn_options, self.options_rect)
            self.tela.blit(self.btn_exit, self.exit_rect)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
