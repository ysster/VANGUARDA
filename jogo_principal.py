import pygame
from player import Player, Inimigo, Tiro 

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill((150, 75, 0))  # cor de terra
        self.rect = self.image.get_rect(topleft=(x, y))

    def desenhar(self, tela, deslocamento_x):
        tela.blit(self.image, (self.rect.x - deslocamento_x, self.rect.y))

class Jogo:
    def __init__(self, personagem_escolhido="char_a"): 
        pygame.init()
        self.largura, self.altura = 1000, 600
        pygame.mixer.music.stop() 
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("VANGUARDA")
        self.relogio = pygame.time.Clock()

        self.player = Player(100, 400, personagem_escolhido) 
        self.grupo_tiros = self.player.tiros 

        self.plataformas = [
            Plataforma(0, 500, 3000, 30)  
        ]

        self.inimigos = pygame.sprite.Group()
        self.inimigos.add(Inimigo(400, 420, 200))
        self.inimigos.add(Inimigo(1450, 420, 100))
        self.inimigos.add(Inimigo(2050, 420, 100))
        
        self.deslocamento_x = 0
        self.limite_mapa = 3000 
        self.jogando = True

    def executar(self):
        while self.jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jogando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    self.jogando = False

            teclas = pygame.key.get_pressed()
            self.player.update(teclas, self.plataformas, self.inimigos)

            if self.player.rect.left < 0:
                self.player.rect.left = 0
            elif self.player.rect.right > self.limite_mapa:
                self.player.rect.right = self.limite_mapa

            for inimigo in self.inimigos:
                inimigo.update(self.plataformas, self.player)

            self.deslocamento_x = self.player.rect.centerx - self.largura // 2
            if self.deslocamento_x < 0:
                self.deslocamento_x = 0
            elif self.deslocamento_x > self.limite_mapa - self.largura:
                self.deslocamento_x = self.limite_mapa - self.largura

            if self.player.rect.top > self.altura:
                print("Você caiu! Game Over!")
                self.jogando = False

            self.tela.fill((135, 206, 235))  

            for p in self.plataformas:
                p.desenhar(self.tela, self.deslocamento_x)

            for inimigo in self.inimigos:
                inimigo.desenhar(self.tela, self.deslocamento_x)
            
            for tiro in self.grupo_tiros:
                tiro.desenhar(self.tela, self.deslocamento_x)

            self.player.desenhar(self.tela)

            pygame.display.flip()
            self.relogio.tick(60)

        pygame.quit()
