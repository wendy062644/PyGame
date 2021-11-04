import pygame
import os

from pygame import draw
from pygame.constants import K_SPACE

FPS = 60
TIME = 0

WIDTH = 500
HEIGHT = 600

pygame.init() #初始化
pygame.mixer.init
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

pygame.display.set_caption("遊戲")

background_img = pygame.image.load(os.path.join("image", "background.png")).convert()
player_img = pygame.image.load(os.path.join("image", "player.png")).convert()
boss_img = pygame.image.load(os.path.join("image", "boss.png")).convert()

shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
damaged_sound = pygame.mixer.Sound(os.path.join("sound", "damaged.wav"))

font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_lobby():
    draw_text(screen, '大戰外星人', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '遊戲說明: → 右移  ← 左移  空白鍵攻擊', 25, WIDTH/2, HEIGHT/2-30)
    draw_text(screen, '-按任意建開始-', 30, WIDTH/2, HEIGHT-100)
    pygame.display.update()
    waitting = True
    while waitting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waitting = False
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waitting = False

def draw_end():
    screen.blit(background_img, (0, 0))
    draw_text(screen, '你的分數: ', 48, WIDTH/2, HEIGHT/4)
    draw_text(screen, '-按任意鍵結束遊戲-', 30, WIDTH/2, HEIGHT-100)
    pygame.display.update()
    waitting = True
    while waitting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waitting = False
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waitting = False
                pygame.quit()



def print_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = WIDTH-20 
    BAR_HEIGTH = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGTH)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGTH)
    pygame.draw.rect(surf, (0, 255, 0), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

def print_bosshealth(surf, bosshp, x, y):
    if bosshp < 0:
        bosshp = 0
    BAR_LENGTH = WIDTH-20 
    BAR_HEIGTH = 10
    fill = (bosshp/500)*BAR_LENGTH
    outline_rect = pygame.Rect(10, 1, BAR_LENGTH, BAR_HEIGTH)
    fill_rect = pygame.Rect(10, 1, fill, BAR_HEIGTH)
    pygame.draw.rect(surf, (255, 0 , 0), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 70))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (250, HEIGHT-55)
        self.MoveX = 5
        self.health = 100

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] and self.rect.x < WIDTH-70:
            self.rect.x += self.MoveX
        if key_pressed[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.MoveX  

    def Pattack(self):
        Pbullet = PlayerAttack(self.rect.centerx, self.rect.top)
        all_sprites.add(Pbullet)
        PlayerBullet.add(Pbullet)
        shoot_sound.play()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss_img, (150, 70))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.y = 30
        self.BossMove = 3
        self.health = 500

    def update(self):
        self.rect.x += self.BossMove
        if self.rect.x > WIDTH-150:
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

show_lobby = True

while running:

    if show_lobby:
        draw_lobby()
        show_lobby = False

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

    hits = pygame.sprite.spritecollide(player, BossBullet, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= 10
        damaged_sound.play()
        if player.health == 0:
            running = False
            

    bosshits = pygame.sprite.spritecollide(boss, PlayerBullet, True, pygame.sprite.collide_circle)
    for hit in bosshits:
        boss.health -= 10
        damaged_sound.play()

    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    print_health(screen, player.health, 10, HEIGHT-15)
    print_bosshealth(screen, boss.health, 10, HEIGHT-15)
    pygame.display.update()
    
    if player.health == 0:
        draw_end()
pygame.quit()
