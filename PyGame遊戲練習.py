import pygame
import os

FPS = 60
TIME = 0

WIDTH = 500
HEIGHT = 600

pygame.init() #初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

pygame.display.set_caption("遊戲")

background_img = pygame.image.load(os.path.join("image", "background.png")).convert()
player_img = pygame.image.load(os.path.join("image", "player.png")).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 70))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (250, HEIGHT-35)
        self.MoveX = 5

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] and self.rect.x < WIDTH-40:
            self.rect.x += self.MoveX
        if key_pressed[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.MoveX  

    def Pattack(self):
        Pbullet = PlayerAttack(self.rect.centerx, self.rect.top)
        all_sprites.add(Pbullet)
        PlayerBullet.add(Pbullet)

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 60))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.y = 0
        self.BossMove = 3

    def update(self):
        self.rect.x += self.BossMove
        if self.rect.x > WIDTH-100:
            self.BossMove = -3
        if self.rect.x < 0:
            self.BossMove = 3

    def Battack(self):
        Bbullet = BossAttack(self.rect.x, self.rect.y)
        all_sprites.add(Bbullet)
        BossBullet.add(Bbullet)

class PlayerAttack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 30))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.Speed = -10

    def update(self):
        self.rect.y += self.Speed
        if self.rect.y < 0:
            self.kill()

class BossAttack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 35))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 50
        self.rect.bottom = y + 85
        self.Speed = 10

    def update(self):
        self.rect.y += self.Speed
        if self.rect.y > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
PlayerBullet = pygame.sprite.Group()
BossBullet = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
boss = Boss()
all_sprites.add(boss)

while running:

    TIME += 1

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.Pattack()
    
    if TIME == 40:
        boss.Battack()
        TIME = 0

    all_sprites.update()
    pygame.sprite.groupcollide(PlayerBullet, BossBullet, True, True)

    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
