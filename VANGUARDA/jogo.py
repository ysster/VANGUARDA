import pygame
import sys

pygame.init()
pygame.mixer.init()

class Menu:
    def __init__(self):
        self.largura, self.altura = 1000, 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("VANGUARDA")

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.VERDE = (0, 200, 0)

        self.fonte = pygame.font.SysFont(None, 32)

        try:
            pygame.mixer.music.load('Three.mp3')
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
        except:
            pass

        try:
            self.fundo = pygame.image.load("Fundo.png")
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
            self.tem_fundo = True
        except:
            self.tem_fundo = False

        largura_botao = 300
        altura_botao = 60
        distancia = 10

        total_altura_botoes = altura_botao * 3 + distancia * 2
        pos_y_inicial = (self.altura - total_altura_botoes) // 2

        self.botao_jogar = pygame.Rect(
            (self.largura - largura_botao) // 2,
            pos_y_inicial,
            largura_botao,
            altura_botao
        )
        self.botao_instrucoes = pygame.Rect(
            self.botao_jogar.x,
            self.botao_jogar.bottom + distancia,
            largura_botao,
            altura_botao
        )
        self.botao_sair = pygame.Rect(
            self.botao_jogar.x,
            self.botao_instrucoes.bottom + distancia,
            largura_botao,
            altura_botao
        )

        self.bg_botoes = pygame.Surface(
            (largura_botao + 40, total_altura_botoes + 40),
            pygame.SRCALPHA
        )
        self.bg_botoes.fill((0, 0, 0, 150))

    def desenhar_botao(self, ret, texto, cor_fundo, cor_texto):
        pygame.draw.rect(self.tela, cor_fundo, ret, border_radius=8)
        pygame.draw.rect(self.tela, self.PRETO, ret, 3, border_radius=8)
        txt = self.fonte.render(texto, True, cor_texto)
        self.tela.blit(
            txt,
            (ret.x + (ret.width - txt.get_width()) // 2,
             ret.y + (ret.height - txt.get_height()) // 2)
        )

    def rodar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.botao_jogar.collidepoint(evento.pos):
                        pass
                    elif self.botao_instrucoes.collidepoint(evento.pos):
                        pass
                    elif self.botao_sair.collidepoint(evento.pos):
                        rodando = False

            if self.tem_fundo:
                self.tela.blit(self.fundo, (0, 0))
            else:
                self.tela.fill((50, 50, 50))

            self.tela.blit(self.bg_botoes, (self.botao_jogar.x - 20, self.botao_jogar.y - 20))

            self.desenhar_botao(self.botao_jogar, "JOGAR", self.VERDE, self.BRANCO)
            self.desenhar_botao(self.botao_instrucoes, "INSTRUÇÕES", self.BRANCO, self.PRETO)
            self.desenhar_botao(self.botao_sair, "SAIR", self.BRANCO, self.PRETO)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    menu = Menu()
    menu.rodar()
