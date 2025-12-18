import pygame
import os

# ================== PLAYER ==================
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, personagem_escolhido="char_a"):
        super().__init__()

        # ================= MOVIMENTO =================
        self.velocidade = 5
        self.gravidade = 0.8
        self.forca_pulo = -16
        self.no_chao_flag = False
        self.vel_y = 0
        self.direcao = 1

        # ================= VIDA (CORAÇÕES) =================
        self.max_coracoes = 5
        self.coracoes = 5
        self.vida_por_coracao = 20

        self.invulneravel = False
        self.tempo_invulneravel = 0

        # ================= ATAQUE =================
        self.atacando = False
        self.tempo_ataque = 0

        # ================= PERSONAGEM =================
        if personagem_escolhido == "char_b":
            nome_arquivo = "Escolhamenina.png"
        else:
            nome_arquivo = "Escolhamenino.png"

        caminho = os.path.join("assets", nome_arquivo)
        self.image_original = pygame.image.load(caminho).convert_alpha()

        # 🔥 TAMANHO GRANDE
        self.image_original = pygame.transform.scale(self.image_original, (120, 180))
        self.image = self.image_original.copy()

        self.rect = self.image.get_rect(topleft=(x, y))

        # ================= CORAÇÕES =================
        self.img_coracao_cheio = pygame.transform.scale(
            pygame.image.load(os.path.join("assets/Coraçãocheio.png")).convert_alpha(),
            (36, 36)
        )
        self.img_coracao_vazio = pygame.transform.scale(
            pygame.image.load(os.path.join("assets/Coraçãovazio.png")).convert_alpha(),
            (36, 36)
        )

    # ================= FÍSICA =================
    def aplicar_gravidade(self, plataformas):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y
        self.no_chao_flag = False

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.no_chao_flag = True

        if self.rect.bottom >= 700:
            self.rect.bottom = 700
            self.vel_y = 0
            self.no_chao_flag = True

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
            self.direcao = -1
            self.image = pygame.transform.flip(self.image_original, True, False)

        elif teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
            self.direcao = 1
            self.image = self.image_original.copy()

        if teclas[pygame.K_UP] and self.no_chao_flag:
            self.vel_y = self.forca_pulo

    # ================= ATAQUE =================
    def atacar(self, inimigos):
        if not self.atacando:
            self.atacando = True
            self.tempo_ataque = 15

            area = pygame.Rect(
                self.rect.centerx + (70 * self.direcao),
                self.rect.y + 30,
                80,
                self.rect.height - 60
            )

            for inimigo in inimigos:
                if area.colliderect(inimigo.rect):
                    inimigo.levar_dano(20)

    def levar_dano(self, dano):
        if not self.invulneravel:
            self.coracoes -= dano // self.vida_por_coracao
            if self.coracoes < 0:
                self.coracoes = 0
            self.invulneravel = True
            self.tempo_invulneravel = 60

    def update(self, teclas, plataformas, inimigos):
        self.mover(teclas)
        self.aplicar_gravidade(plataformas)

        if teclas[pygame.K_SPACE]:
            self.atacar(inimigos)

        if self.atacando:
            self.tempo_ataque -= 1
            if self.tempo_ataque <= 0:
                self.atacando = False

        if self.invulneravel:
            self.tempo_invulneravel -= 1
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False

    def desenhar(self, tela):
        if not self.invulneravel or self.tempo_invulneravel % 10 < 5:
            tela.blit(self.image, self.rect)
        self.desenhar_coracoes(tela)

    def desenhar_coracoes(self, tela):
        x, y = 20, 20
        for i in range(self.max_coracoes):
            if i < self.coracoes:
                tela.blit(self.img_coracao_cheio, (x, y))
            else:
                tela.blit(self.img_coracao_vazio, (x, y))
            x += 40


# ================== INIMIGO ==================
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, alcance=120):
        super().__init__()

        self.vida = 50
        self.velocidade = 2
        self.gravidade = 0.8
        self.vel_y = 0

        self.x_inicial = x
        self.x_final = x + alcance
        self.direcao = 1

        self.image = pygame.image.load(
            os.path.join("assets/Escolhamenina.png")
        ).convert_alpha()

        # 🔥 TAMANHO GRANDE
        self.image = pygame.transform.scale(self.image, (120, 180))
        self.rect = self.image.get_rect(topleft=(x, y))

    def aplicar_gravidade(self, plataformas):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0

        if self.rect.bottom >= 700:
            self.rect.bottom = 700
            self.vel_y = 0

    def levar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.kill()

    def update(self, plataformas, player):
        self.rect.x += self.velocidade * self.direcao
        if self.rect.x >= self.x_final or self.rect.x <= self.x_inicial:
            self.direcao *= -1

        self.aplicar_gravidade(plataformas)

        if self.rect.colliderect(player.rect) and not player.invulneravel:
            player.levar_dano(20)

    def desenhar(self, tela, dx):
        tela.blit(self.image, (self.rect.x - dx, self.rect.y))
