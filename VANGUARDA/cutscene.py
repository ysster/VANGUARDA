import pygame
import sys

class Cutscene:
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.largura = largura
        self.altura = altura

        self.fundos = [
            pygame.transform.scale(
                pygame.image.load("assets/cutscene/Imagem1.png").convert(),
                (largura, altura)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/cutscene/Imagem2.png").convert(),
                (largura, altura)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/cutscene/Imagem2.png").convert(),
                (largura, altura)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/cutscene/Imagem2.png").convert(),
                (largura, altura)
            )
        ]

        self.textos = [
            "Em um mundo à beira do colapso...",
            "Uma força desconhecida se aproxima.",
            "O destino de todos será decidido.",
            "A jornada comeca agora."
        ]

        self.fonte = pygame.font.Font(None, 36)

        self.cena_atual = 0
        self.caracteres = 0.0

        self.velocidade_texto = 0.2
        self.tempo_espera = 2000
        self.tempo_inicio = pygame.time.get_ticks()

        # FADE
        self.fade_alpha = 0
        self.fazendo_fade = False
        self.fade_direcao = 1  # 1 = escurecer, -1 = clarear
        self.overlay = pygame.Surface((largura, altura))
        self.overlay.fill((0, 0, 0))

    def executar(self):
        clock = pygame.time.Clock()
        rodando = True

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            agora = pygame.time.get_ticks()

            # fundo
            self.tela.blit(self.fundos[self.cena_atual], (0, 0))

            # texto
            texto_render = self.fonte.render(
                self.textos[self.cena_atual][:int(self.caracteres)],
                True,
                (255, 255, 255)
            )
            self.tela.blit(texto_render, (60, self.altura - 100))

            # escrita automática
            if not self.fazendo_fade:
                if self.caracteres < len(self.textos[self.cena_atual]):
                    self.caracteres += self.velocidade_texto
                    self.tempo_inicio = agora
                else:
                    if agora - self.tempo_inicio >= self.tempo_espera:
                        self.fazendo_fade = True
                        self.fade_direcao = 1
                        self.fade_alpha = 0

            # FADE
            if self.fazendo_fade:
                self.fade_alpha += 8 * self.fade_direcao
                self.fade_alpha = max(0, min(255, self.fade_alpha))
                self.overlay.set_alpha(self.fade_alpha)
                self.tela.blit(self.overlay, (0, 0))

                if self.fade_alpha >= 255:
                    self.cena_atual += 1
                    self.caracteres = 0.0
                    self.fade_direcao = -1

                    if self.cena_atual >= len(self.textos):
                        return

                if self.fade_alpha <= 0 and self.fade_direcao == -1:
                    self.fazendo_fade = False
                    self.tempo_inicio = agora

            pygame.display.update()
            clock.tick(60)
