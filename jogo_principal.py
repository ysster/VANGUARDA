import pygame
from player import Player, Inimigo
import os

# ================== PLATAFORMA (GRAMA) ==================
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, imagem):
        super().__init__()

        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)

        bloco_largura = imagem.get_width()
        bloco_altura = imagem.get_height()

        # Repetir o bloco de grama horizontalmente
        for i in range(0, largura, bloco_largura):
            self.image.blit(imagem, (i, 0))

        self.rect = self.image.get_rect(topleft=(x, y))

    def desenhar(self, tela, dx):
        tela.blit(self.image, (self.rect.x - dx, self.rect.y))


# ================== JOGO ==================
class Jogo:
    def __init__(self, personagem="char_a"):
        pygame.init()
        pygame.mixer.init()

        self.largura, self.altura = 1400, 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("VANGUARDA")

        self.relogio = pygame.time.Clock()

        # ================= FUNDO =================
        self.fundo = pygame.image.load(
            os.path.join("assets", "Fundo.jpg")
        ).convert()

        largura_original, altura_original = self.fundo.get_size()
        escala = self.altura / altura_original
        largura_nova = int(largura_original * escala)
        self.fundo = pygame.transform.scale(self.fundo, (largura_nova, self.altura))

        # Overlay para suavizar fundo
        self.overlay = pygame.Surface((self.largura, self.altura))
        self.overlay.set_alpha(60)
        self.overlay.fill((0, 0, 0))

        # ================= MÚSICA =================
        musica = os.path.join("assets", "musica_jogo.mp3")
        if os.path.exists(musica):
            pygame.mixer.music.load(musica)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

        # ================= GRAMA =================
        self.img_grama = pygame.image.load(
            os.path.join("assets", "grama.png")
        ).convert_alpha()

        # Se quiser ajustar tamanho do bloco:
        self.img_grama = pygame.transform.scale(self.img_grama, (128, 128))

        # ================= PLAYER =================
        self.player = Player(200, 400, personagem)

        # ================= MAPA =================
        self.limite_mapa = 3000

        self.plataformas = [
            Plataforma(0, 700, self.limite_mapa, 128, self.img_grama)
        ]

        # ================= INIMIGOS =================
        self.inimigos = pygame.sprite.Group()
        self.inimigos.add(Inimigo(600, 520, 200))
        self.inimigos.add(Inimigo(1400, 520, 150))
        self.inimigos.add(Inimigo(2200, 520, 150))

        self.dx = 0
        self.jogando = True

    def executar(self):
        while self.jogando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.jogando = False

            teclas = pygame.key.get_pressed()

            # ================= UPDATE =================
            self.player.update(teclas, self.plataformas, self.inimigos)

            for inimigo in self.inimigos:
                inimigo.update(self.plataformas, self.player)

            # ================= CAMERA =================
            self.dx = self.player.rect.centerx - self.largura // 2
            self.dx = max(0, min(self.dx, self.limite_mapa - self.largura))

            # ================= DESENHO =================
            self.tela.fill((0, 0, 0))

            # FUNDO (parallax)
            x_fundo = int(-self.dx * 0.5)
            while x_fundo < self.largura:
                self.tela.blit(self.fundo, (x_fundo, 0))
                x_fundo += self.fundo.get_width()

            # Overlay
            self.tela.blit(self.overlay, (0, 0))

            # PLATAFORMAS (GRAMA)
            for p in self.plataformas:
                p.desenhar(self.tela, self.dx)

            # INIMIGOS
            for inimigo in self.inimigos:
                inimigo.desenhar(self.tela, self.dx)

            # PLAYER
            self.player.desenhar(self.tela)

            pygame.display.flip()
            self.relogio.tick(60)

        pygame.quit()
