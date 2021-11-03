import pygame

FPS = 60

WIDTH = 500
HEIGHT = 600

pygame.init() #初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

pygame.display.set_caption("遊戲")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (250, HEIGHT-35)
        self.MoveX = 5

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] and self.rect.x < WIDTH-40:
            self.rect.x += self.MoveX
        if key_pressed[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.MoveX  


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.y = 0
        self.BossMove = 3

    def update(self):
        self.rect.x += self.BossMove
        if self.rect.x > WIDTH-30:
            self.BossMove = -3
        if self.rect.x < 0:
            self.BossMove = 3


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
boss = Boss()
all_sprites.add(boss)

while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()


    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
