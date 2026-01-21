import pygame
from player import Player, Inimigo, Tiro

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill((150, 75, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def desenhar(self, tela, dx):
        tela.blit(self.image, (self.rect.x - dx, self.rect.y))


class Jogo:
    def __init__(self, personagem="char_a"):
        pygame.init()

        self.largura, self.altura = 1400, 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))

        pygame.display.set_caption("VANGUARDA")

        self.relogio = pygame.time.Clock()

        self.player = Player(100, 400, personagem)
        self.grupo_tiros = self.player.tiros

        self.plataformas = [
            Plataforma(0, 700, 3000, 150)
        ]

        self.inimigos = pygame.sprite.Group()
        self.inimigos.add(Inimigo(400, 620, 200))
        self.inimigos.add(Inimigo(1450, 620, 100))
        self.inimigos.add(Inimigo(2050, 620, 100))

        self.dx = 0
        self.limite_mapa = 3000
        self.jogando = True

    def executar(self):

        while self.jogando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.jogando = False

            teclas = pygame.key.get_pressed()
            self.player.update(teclas, self.plataformas, self.inimigos)
            self.dx = self.player.rect.centerx - self.largura // 2
            self.dx = max(0, min(self.dx, self.limite_mapa - self.largura))

            self.tela.fill((135, 206, 235))

            for p in self.plataformas:
                p.desenhar(self.tela, self.dx)

            for inimigo in self.inimigos:
                inimigo.update(self.plataformas, self.player)
                inimigo.desenhar(self.tela, self.dx)

            for t in self.grupo_tiros:
                t.desenhar(self.tela, self.dx)

            self.player.desenhar(self.tela)

            pygame.display.flip()
            self.relogio.tick(60)

        pygame.quit()
