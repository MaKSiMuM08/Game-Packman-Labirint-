# Разработай свою игру в этом файл
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, x_speed, y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = p.rect.left
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = p.rect.right
        elif self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = p.rect.bottom   
    def fire(self):
        bullet = Bullet('pacman.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 440:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()


barriers = sprite.Group()
win_width = 700
win_height = 500
display.set_caption('Лабиринт')
window =  display.set_mode((win_width, win_height))
wall1 = GameSprite('wall.png', win_width/2 - win_width/3, win_height/2, 300, 50)
wall2 = GameSprite('wall.png', 370, 100, 50, 400)
barriers.add(wall1)
barriers.add(wall2)
hero = Player('monster.png', 5, win_height - 80, 80, 80, 0, 0)
final = GameSprite('pacman.png', win_width - 85, win_height - 100, 80, 80)

monster1 = Enemy('monster1.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('monster1.png', win_width - 80, 240, 80, 80, 5)
monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)

bullets = sprite.Group()


back = (119, 210, 223)
finish = False
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                hero.x_speed = -5
            elif e.key == K_RIGHT:
                hero.x_speed = 5
            elif e.key == K_UP:
                hero.y_speed = -5
            elif e.key == K_DOWN:
                hero.y_speed = 5
            elif e.key == K_SPACE:
                hero.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                hero.x_speed = 0
            elif e.key == K_RIGHT:
                hero.x_speed = 0
            elif e.key == K_UP:
                hero.y_speed = 0
            elif e.key == K_DOWN:
                hero.y_speed = 0
    if finish != True:
        window.fill(back)
        barriers.draw(window)
        hero.reset()
        hero.update()
        bullets.update()
        bullets.draw(window)
        final.reset()
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(barriers, bullets, False, True)
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            img = image.load('lose.jpg')
            window.blit(transform.scale(img, (700, 500)), (0, 0))
        if sprite.collide_rect(hero, final):
            finish = True
            img = image.load('win.jpg')
            window.blit(transform.scale(img, (700, 500)), (0, 0))
    display.update()

