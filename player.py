import pygame
import os

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao=1):
        super().__init__()
        self.image = pygame.Surface((15, 5))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 10 * direcao 
        self.direcao = direcao

    def update(self):
        self.rect.x += self.velocidade

        if self.rect.x > 3000 or self.rect.x < -1000: 
            self.kill()
            
    def desenhar(self, tela, deslocamento_x):

        tela.blit(self.image, (self.rect.x - deslocamento_x, self.rect.y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, personagem_escolhido="char_a"):
        self.velocidade = 5
        self.gravidade = 0.8
        self.forca_pulo = -15
        self.no_chao = False
        self.vida_max = 100
        self.vida = 100
        self.municao_max = 25
        self.municao = 25
        self.tempo_recarga = 0
        self.invulneravel = False
        self.tempo_invulneravel = 0
        self.direcao = 1
 
        if personagem_escolhido == "char_b":
            nome_arquivo = "Personagemmenina.png" 
            cor_padrao = (255, 105, 180) 
        else:
            nome_arquivo = "Personagemmenino.png" 
            cor_padrao = (0, 255, 0) 
        
        caminho_imagem = os.path.join("assets", nome_arquivo)
        try:

            self.image_original = pygame.image.load(caminho_imagem).convert_alpha()
        except:
            print(f"Aviso: Imagem '{nome_arquivo}' não encontrada. Usando cor padrão.")
            self.image_original = pygame.Surface((50, 80))
            self.image_original.fill(cor_padrao)
        
        self.image_original = pygame.transform.scale(self.image_original, (50, 80))
        self.image = self.image_original.copy()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.tiros = pygame.sprite.Group()

    def aplicar_gravidade(self, plataformas):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y
        self.no_chao = False

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0:
                    self.rect.top = plataforma.rect.bottom
                    self.vel_y = 0

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.no_chao = True

    def mover(self, teclas):
        if teclas[pygame.K_a]: # Usando A e D para movimento lateral
            self.rect.x -= self.velocidade
            self.direcao = -1
            self.image = pygame.transform.flip(self.image_original, True, False)
        elif teclas[pygame.K_d]:
            self.rect.x += self.velocidade
            self.direcao = 1
            self.image = self.image_original.copy()
        
        # Pulo
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False

    def atirar(self):
        if self.municao > 0 and self.tempo_recarga == 0:
            offset = 40 * self.direcao
            tiro = Tiro(self.rect.centerx + offset, self.rect.centery, self.direcao) 
            self.tiros.add(tiro)
            self.municao -= 1
            self.tempo_recarga = 15

    def levar_dano(self, dano):
        if not self.invulneravel:
            self.vida -= dano
            self.invulneravel = True
            self.tempo_invulneravel = 60
            if self.vida <= 0:
                self.vida = 0
                print("Jogador derrotado!")

    def update(self, teclas, plataformas, inimigos_grupo=pygame.sprite.Group()):
        self.mover(teclas)
        self.aplicar_gravidade(plataformas)
        self.tiros.update()
        
        if self.invulneravel:
            self.tempo_invulneravel -= 1
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False
        
        # Atirar
        if teclas[pygame.K_j]: # Usando 'J' para atirar
            self.atirar()

        # Cooldown do Tiro
        if self.tempo_recarga > 0:
            self.tempo_recarga -= 1
        
        # Colisão de Tiros com Inimigos (Usando groupcollide para melhor performance)
        colisoes = pygame.sprite.groupcollide(self.tiros, inimigos_grupo, True, False)
        for tiro, inimigo_lista in colisoes.items():
            for inimigo in inimigo_lista:
                inimigo.levar_dano(10)

    def desenhar(self, tela):
        # O player é desenhado sem deslocamento X, pois o mundo se move ao seu redor
        if not self.invulneravel or self.tempo_invulneravel % 10 < 5:
            tela.blit(self.image, self.rect)
        self.desenhar_hud(tela)

    def desenhar_hud(self, tela):
        fonte = pygame.font.SysFont(None, 30)
        pygame.draw.rect(tela, (255, 0, 0), (20, 20, 200, 20))
        pygame.draw.rect(tela, (0, 255, 0), (20, 20, 200 * (self.vida / self.vida_max), 20))
        texto_municao = fonte.render(f"Munição: {self.municao}/{self.municao_max}", True, (0, 0, 0))
        tela.blit(texto_municao, (20, 50))


# ----------------------------------------------------------------------
# CLASSE INIMIGO (Mantida a mesma)
# ----------------------------------------------------------------------
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, alcance_movimento=100):
        super().__init__()
        self.vida_max = 50
        self.vida = 50
        self.dano = 20
        self.velocidade = 2
        self.gravidade = 0.8
        self.vel_y = 0
        self.no_chao = False
        
        self.x_inicial = x
        self.x_final = x + alcance_movimento
        self.direcao = 1
        
        caminho_imagem = os.path.join("assets", "Inimigo.png") # CORRIGIDO: Adiciona .png
        try:
            self.image = pygame.image.load(caminho_imagem).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 80))
        except:
            self.image = pygame.Surface((50, 80))
            self.image.fill((255, 0, 0)) 
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def aplicar_gravidade(self, plataformas):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y
        self.no_chao = False

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0:
                    self.rect.top = plataforma.rect.bottom
                    self.vel_y = 0

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.no_chao = True

    def levar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.kill() 

    def update(self, plataformas, player):
        
        if self.direcao == 1:
            self.rect.x += self.velocidade
            if self.rect.right >= self.x_final:
                self.direcao = -1
        else:
            self.rect.x -= self.velocidade
            if self.rect.left <= self.x_inicial:
                self.direcao = 1

        self.aplicar_gravidade(plataformas)
        
        if self.rect.colliderect(player.rect) and not player.invulneravel:
            player.levar_dano(self.dano)
        
    def desenhar(self, tela, deslocamento_x):
        tela.blit(self.image, (self.rect.x - deslocamento_x, self.rect.y))