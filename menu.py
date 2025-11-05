import pygame
import sys
import os # Importar para carregar imagens
from jogo_principal import Jogo

pygame.init()
pygame.mixer.init()

# ----------------------------------------------------------------------
# CLASSE: SelecaoPersonagem (NOVA TELA)
# ----------------------------------------------------------------------
class SelecaoPersonagem:
    def __init__(self, tela, largura, altura, fonte):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.fonte = fonte
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AZUL_ESCURO = (50, 70, 80, 180) # Cor da caixa de diálogo
        self.VERDE_CLARO = (173, 216, 230) 
        self.COR_DESTAQUE = (0, 255, 0) 

        # Dimensões da Caixa de Diálogo
        largura_painel = 800
        altura_painel = 400
        x_painel = (largura - largura_painel) // 2
        y_painel = (altura - altura_painel) // 2

        self.painel_rect = pygame.Rect(x_painel, y_painel, largura_painel, altura_painel)
        self.bg_painel = pygame.Surface((largura_painel, altura_painel), pygame.SRCALPHA)
        self.bg_painel.fill((0, 0, 0, 180)) # Fundo semi-transparente

        # Chaves de identificação interna
        self.CHAR_A = "char_a" 
        self.CHAR_B = "char_b" 
        
        # Aumenta o tamanho dos sprites (Aprox. 1.5x o tamanho original de 50x80 no jogo)
        TAM_SPRITE_X, TAM_SPRITE_Y = 100, 160 
        
        # Posições das Imagens (Centralizadas dentro do painel)
        x_central = x_painel + largura_painel // 2
        distancia_entre_chars = 150 # Distância do centro para cada personagem
        y_chars = y_painel + 150 # Posição vertical abaixo do título

        # Rects Clicáveis (Aumentados um pouco para facilitar o clique)
        self.rect_char1 = pygame.Rect(x_central - distancia_entre_chars - TAM_SPRITE_X//2, y_chars - 10, TAM_SPRITE_X + 20, TAM_SPRITE_Y + 20)
        self.rect_char2 = pygame.Rect(x_central + distancia_entre_chars - TAM_SPRITE_X//2, y_chars - 10, TAM_SPRITE_X + 20, TAM_SPRITE_Y + 20)
        
        # --- Carrega imagens dos personagens ---
        # Tenta carregar Personagem A (menino)
        try:
            self.img_char1 = pygame.image.load(os.path.join("assets", "Personagemmenino.png")).convert_alpha()
            self.img_char1 = pygame.transform.scale(self.img_char1, (TAM_SPRITE_X, TAM_SPRITE_Y))
        except:
            self.img_char1 = pygame.Surface((TAM_SPRITE_X, TAM_SPRITE_Y))
            self.img_char1.fill(self.VERDE_CLARO)
            
        # Tenta carregar Personagem B (menina)
        try:
            self.img_char2 = pygame.image.load(os.path.join("assets", "Personagemmenina.png")).convert_alpha()
            self.img_char2 = pygame.transform.scale(self.img_char2, (TAM_SPRITE_X, TAM_SPRITE_Y))
        except:
            self.img_char2 = pygame.Surface((TAM_SPRITE_X, TAM_SPRITE_Y))
            self.img_char2.fill(self.COR_DESTAQUE)

    def desenhar_painel_selecao(self, mouse_pos):
        # Desenha a caixa de diálogo
        self.tela.blit(self.bg_painel, self.painel_rect.topleft)

        # Desenha Título
        titulo = self.fonte.render("Escolha Seu Personagem", True, self.BRANCO)
        self.tela.blit(titulo, (self.painel_rect.x + (self.painel_rect.width - titulo.get_width()) // 2, 
                                 self.painel_rect.y + 40))

        # --------------------- Personagem 1 (CHAR_A) ---------------------
        # Desenha o retangulo clicável (highlight)
        cor_highlight_1 = self.COR_DESTAQUE if self.rect_char1.collidepoint(mouse_pos) else (50, 50, 50, 0)
        pygame.draw.rect(self.tela, cor_highlight_1, self.rect_char1, 3, border_radius=5)
        
        # Desenha Imagem 1
        self.tela.blit(self.img_char1, self.rect_char1.topleft)
        
        # --------------------- Personagem 2 (CHAR_B) ---------------------
        # Desenha o retangulo clicável (highlight)
        cor_highlight_2 = self.COR_DESTAQUE if self.rect_char2.collidepoint(mouse_pos) else (50, 50, 50, 0)
        pygame.draw.rect(self.tela, cor_highlight_2, self.rect_char2, 3, border_radius=5)
        
        # Desenha Imagem 2
        self.tela.blit(self.img_char2, self.rect_char2.topleft)
        
    def rodar(self, tela_fundo):
        rodando = True
        personagem_escolhido = None

        while rodando:
            mouse_pos = pygame.mouse.get_pos()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    return None # Volta para o menu principal
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: # Botão esquerdo
                    if self.rect_char1.collidepoint(evento.pos):
                        personagem_escolhido = self.CHAR_A 
                        rodando = False
                    elif self.rect_char2.collidepoint(evento.pos):
                        personagem_escolhido = self.CHAR_B
                        rodando = False

            self.tela.blit(tela_fundo, (0, 0)) # Desenha o fundo do menu
            self.desenhar_painel_selecao(mouse_pos)
            
            pygame.display.flip()
        
        return personagem_escolhido


# ----------------------------------------------------------------------
# CLASSE: Menu (Adiciona chamada para a tela de seleção)
# ----------------------------------------------------------------------
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
            pygame.mixer.music.load('assets/Three.mp3')
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
        except:
            pass

        try:
            self.fundo = pygame.image.load("assets/Fundo.png")
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
            self.tem_fundo = True
            self.tela_fundo_menu = self.fundo.copy() # Salva o fundo para passar para a tela de seleção
        except:
            self.tem_fundo = False
            self.tela_fundo_menu = pygame.Surface((self.largura, self.altura))
            self.tela_fundo_menu.fill((50, 50, 50))


        largura_botao = 300
        altura_botao = 60
        distancia = 10
        total_altura_botoes = altura_botao * 3 + distancia * 2
        pos_y_inicial = (self.altura - total_altura_botoes) // 2

        self.botao_jogar = pygame.Rect((self.largura - largura_botao) // 2, pos_y_inicial, largura_botao, altura_botao)
        self.botao_instrucoes = pygame.Rect(self.botao_jogar.x, self.botao_jogar.bottom + distancia, largura_botao, altura_botao)
        self.botao_sair = pygame.Rect(self.botao_jogar.x, self.botao_instrucoes.bottom + distancia, largura_botao, altura_botao)

        self.bg_botoes = pygame.Surface((largura_botao + 40, total_altura_botoes + 40), pygame.SRCALPHA)
        self.bg_botoes.fill((0, 0, 0, 150))
        
        # Inicializa a tela de seleção
        self.selecao_personagem = SelecaoPersonagem(self.tela, self.largura, self.altura, self.fonte)

    def desenhar_botao(self, ret, texto, cor_fundo, cor_texto):
        pygame.draw.rect(self.tela, cor_fundo, ret, border_radius=8)
        pygame.draw.rect(self.tela, self.PRETO, ret, 3, border_radius=8)
        txt = self.fonte.render(texto, True, cor_texto)
        self.tela.blit(txt, (ret.x + (ret.width - txt.get_width()) // 2,
                             ret.y + (ret.height - txt.get_height()) // 2))

    def rodar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.botao_jogar.collidepoint(evento.pos):
                        # CHAMA A TELA DE SELEÇÃO
                        escolha = self.selecao_personagem.rodar(self.tela_fundo_menu)
                        if escolha:
                            # CORRIGIDO: Chama Jogo com o argumento de escolha
                            jogo = Jogo(escolha)          
                            jogo.executar()
                            # Quando o jogo terminar, a música do menu é reiniciada
                            pygame.mixer.music.play(-1)
                    elif self.botao_instrucoes.collidepoint(evento.pos):
                        print("Instruções ainda não implementadas.")
                    elif self.botao_sair.collidepoint(evento.pos):
                        rodando = False

            if self.tem_fundo:
                self.tela.blit(self.fundo, (0, 0))
            else:
                self.tela.fill((50, 50, 50))

            self.tela.blit(self.bg_botoes, (self.botao_jogar.x - 20, self.botao_jogar.y - 20))

            mouse_pos = pygame.mouse.get_pos()
            cor_jogar = (0, 255, 0) if self.botao_jogar.collidepoint(mouse_pos) else self.VERDE
            self.desenhar_botao(self.botao_jogar, "JOGAR", cor_jogar, self.BRANCO)
            self.desenhar_botao(self.botao_instrucoes, "INSTRUÇÕES", self.BRANCO, self.PRETO)
            self.desenhar_botao(self.botao_sair, "SAIR", self.BRANCO, self.PRETO)

            pygame.display.flip()

        pygame.quit()
        sys.exit()