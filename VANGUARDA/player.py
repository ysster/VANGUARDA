import pygame
import os


class Player(pygame.sprite.Sprite):
    """
    Player com animações via spritesheet (idle/run/jump/fall).
    Teclas: A/D ou LEFT/RIGHT para andar | W/SPACE/UP para pular
    """

    # ===== AJUSTES RÁPIDOS (se precisar) =====
    SPRITESHEET_PATH = os.path.join("assets/player.png")

    FRAME_W = 64
    FRAME_H = 64

    # Linha do spritesheet (0 = primeira linha), e quantos frames usar
    # Se alguma animação não bater com sua spritesheet, ajuste os ROW_... e COUNT_...
    IDLE_ROW, IDLE_COUNT = 0, 4
    RUN_ROW,  RUN_COUNT  = 1, 6
    JUMP_ROW, JUMP_COUNT = 2, 1
    FALL_ROW, FALL_COUNT = 3, 1

    def __init__(self, x, y, personagem_escolhido="char_a"):
        super().__init__()

        # movimento/física
        self.velocidade = 5
        self.gravidade = 0.8
        self.forca_pulo = -15
        self.vel_y = 0
        self.no_chao = False
        self.direcao = 1  # 1 direita, -1 esquerda

        # vida (mantive do seu)
        self.vida = 100
        self.invulneravel = False
        self.tempo_invulneravel = 0

        # animação
        self.estado = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 100  # ms (velocidade da animação)

        # carrega spritesheet
        self.sheet = self._load_sheet()

        # monta animações
        self.anim = {
            "idle": self._get_frames(self.IDLE_ROW, self.IDLE_COUNT),
            "run":  self._get_frames(self.RUN_ROW,  self.RUN_COUNT),
            "jump": self._get_frames(self.JUMP_ROW, self.JUMP_COUNT),
            "fall": self._get_frames(self.FALL_ROW, self.FALL_COUNT),
        }

        # imagem inicial
        self.image = self.anim["idle"][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # hitbox um pouco mais “justa” (opcional)
        # Se ficar estranho, comente essa linha
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 50, 70)

    def _load_sheet(self):
        try:
            return pygame.image.load(self.SPRITESHEET_PATH).convert_alpha()
        except Exception:
            # fallback (pra não crashar)
            surf = pygame.Surface((self.FRAME_W * 8, self.FRAME_H * 8), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 0, 0), (0, 0, 40, 40))
            return surf

    def _get_frames(self, row, count):
        frames = []
        for i in range(count):
            frame = pygame.Surface((self.FRAME_W, self.FRAME_H), pygame.SRCALPHA)
            frame.blit(
                self.sheet,
                (0, 0),
                (i * self.FRAME_W, row * self.FRAME_H, self.FRAME_W, self.FRAME_H)
            )
            frames.append(frame)
        return frames

    def _set_estado(self, novo):
        if novo != self.estado:
            self.estado = novo
            self.frame_index = 0
            self.frame_timer = 0

    def _mover_x(self, teclas):
        dx = 0

        left = teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        right = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]

        if left:
            dx = -self.velocidade
            self.direcao = -1
        elif right:
            dx = self.velocidade
            self.direcao = 1

        return dx

    def _pular(self, teclas):
        jump = teclas[pygame.K_UP] or teclas[pygame.K_w] or teclas[pygame.K_SPACE]
        if jump and self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False

    def _colisao_x(self, plataformas, dx):
        self.rect.x += dx
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if dx > 0:
                    self.rect.right = p.rect.left
                elif dx < 0:
                    self.rect.left = p.rect.right

    def _colisao_y(self, plataformas):
        self.vel_y += self.gravidade
        if self.vel_y > 20:
            self.vel_y = 20

        self.rect.y += int(self.vel_y)
        self.no_chao = False

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:  # caindo
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0:  # batendo cabeça
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

    def _atualizar_estado(self, dx):
        if not self.no_chao:
            if self.vel_y < 0:
                self._set_estado("jump")
            else:
                self._set_estado("fall")
        else:
            if dx != 0:
                self._set_estado("run")
            else:
                self._set_estado("idle")

    def _animar(self, dt_ms):
        frames = self.anim[self.estado]

        if len(frames) == 1:
            self.frame_index = 0
        else:
            self.frame_timer += dt_ms
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(frames)

        img = frames[self.frame_index]
        if self.direcao == -1:
            img = pygame.transform.flip(img, True, False)

        self.image = img

    def update(self, dt_ms, teclas, plataformas):
        dx = self._mover_x(teclas)
        self._pular(teclas)

        self._colisao_x(plataformas, dx)
        self._colisao_y(plataformas)

        self._atualizar_estado(dx)
        self._animar(dt_ms)

    def desenhar(self, tela, dx_camera):
        # Desenha “colado” no chão pela base da hitbox
        img_rect = self.image.get_rect(midbottom=self.rect.midbottom)
        tela.blit(self.image, (img_rect.x - dx_camera, img_rect.y))
