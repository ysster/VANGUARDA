import pygame
from player import Player


class Plataforma:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.largura, self.altura = 1400, 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("VANGUARDA")
        self.clock = pygame.time.Clock()

        # ======================
        # 🎵 MUSICA DO JOGO
        # ======================
        pygame.mixer.music.load("assets/áudio/audiojogo.mpeg")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        # player (agora com spritesheet/anim)
        self.player = Player(120, 500)

        # fundo
        self.fundo = pygame.transform.scale(
            pygame.image.load("assets/cenário/Fundojogo.png").convert(),
            (self.largura, self.altura)
        )

        # chão (imagem)
        self.chao_img = pygame.image.load("assets/cenário/Chão.png").convert_alpha()
        self.chao_largura = self.chao_img.get_width()
        self.chao_altura = self.chao_img.get_height()

        # ponte (visual)
        self.ponte_img = pygame.image.load("assets/cenário/ponte.png").convert_alpha()

        # mundo / câmera
        self.dx = 0
        self.limite_mapa = 4000

        # ======================
        # FASE 1 — TRAVESSIA DO RIO
        # ======================

        # buracos (x, largura)
        self.buracos = [
            (900, 200),
            (1900, 250),
            (2850, 200),
        ]

        # chão encostado embaixo da tela (topo da imagem)
        self.Y_CHAO = self.altura - self.chao_altura

        # colisão fininha no topo da grama
        self.ALTURA_COLISAO = 20

        # plataformas (NÃO existe chão nos buracos)
        self.plataformas = [
            Plataforma(0, self.Y_CHAO, 900, self.ALTURA_COLISAO),
            Plataforma(1100, self.Y_CHAO, 800, self.ALTURA_COLISAO),
            Plataforma(2150, self.Y_CHAO, 700, self.ALTURA_COLISAO),
            Plataforma(3050, self.Y_CHAO, 950, self.ALTURA_COLISAO),
        ]

        # ponte (visual) no buraco 2
        self.ponte_x = 1900
        self.ponte_y = self.Y_CHAO - 10

        self.rodando = True

    def esta_em_buraco(self, x_mundo: int) -> bool:
        for bx, bw in self.buracos:
            if bx <= x_mundo < bx + bw:
                return True
        return False

    def desenhar_chao(self):
        y_img = self.Y_CHAO

        # desenha a imagem do chão SOMENTE onde existe plataforma (e nunca nos buracos)
        for p in self.plataformas:
            x = p.rect.x
            while x < p.rect.x + p.rect.w:
                if not self.esta_em_buraco(x):
                    self.tela.blit(self.chao_img, (x - self.dx, y_img))
                x += self.chao_largura

    def executar(self):
        while self.rodando:
            dt_ms = self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.rodando = False

            teclas = pygame.key.get_pressed()

            # ✅ UPDATE NOVO (com dt_ms)
            self.player.update(dt_ms, teclas, self.plataformas)

            # câmera
            self.dx = self.player.rect.centerx - self.largura // 2
            self.dx = max(0, min(self.dx, self.limite_mapa - self.largura))

            # desenho
            self.tela.blit(self.fundo, (0, 0))

            # chão (sem imagem nos buracos)
            self.desenhar_chao()

            # ponte (visual)
            self.tela.blit(
                self.ponte_img,
                (self.ponte_x - self.dx, self.ponte_y)
            )

            # player
            self.player.desenhar(self.tela, self.dx)

            pygame.display.flip()

        pygame.mixer.music.stop()
        pygame.quit()
