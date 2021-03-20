import random
import pygame
import pygame.freetype
from tkinter import messagebox

score = 0
angle = 0
level = 1


class Car(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Draw the car (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.image = pygame.image.load("car1.png").convert_alpha()

        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels
        self.rect.y = max(0, min(self.rect.y, 500))

    def move_down(self, pixels):
        self.rect.y += pixels
        self.rect.y = max(0, min(self.rect.y, 500 - self.image.get_height()))

    def update_level(self, level):
        self.image = pygame.image.load(f"car{level}.png").convert_alpha()


class Barrier(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.image = pygame.image.load(f"barrier{level}.png").convert_alpha()

        self.rect = self.image.get_rect()

    def height(self):
        return self.image.get_height()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


pygame.init()

GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

SCREENWIDTH = 800
SCREENHEIGHT = 500

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Racing Fever")

barriers = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()

playerCar = Car(RED, 0, 0)
playerCar.rect.x = 0
playerCar.rect.y = 230

barrier = Barrier(RED, 0, 0)
barrier.rect.x = 400
barrier.rect.y = 230


bg1 = Background('road1.jpg', [0, 0])
bg2 = Background('road2.jpg', [0, 0])
bg3 = Background('road3.jpg', [0, 0])


player.add(playerCar)
barriers.add(barrier)


carryOn = True
clock = pygame.time.Clock()

font = pygame.freetype.Font('font.ttf', 20)
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        playerCar.move_up(5)
    if keys[pygame.K_DOWN]:
        playerCar.move_down(5)
    angle += 1
    angle%=360
    # Game Logic
    if playerCar.rect.colliderect(barrier):
        messagebox.showinfo("Info", f"You died! Score: {score}")
        pygame.quit()
    else:
        barrier.rect.x -= level * 2
        if barrier.rect.x < 0:
            barriers.remove(barrier)
            barrier = Barrier(RED, 0, 0)
            barrier.rect.x = 800
            barrier.rect.y = random.randint(0, 500 - barrier.height())
            barriers.add(barrier)
            score += 1

        barriers.update()

    if score < 5:
        level = 1
    elif score >= 5 and score <= 10:
        level = 2
    else:
        level = 3
    playerCar.update_level(level)


    # Drawing on Screen
    screen.fill(GREEN)
    if level == 1:
        screen.blit(bg1.image, bg1.rect)
    elif level == 2:
        screen.blit(bg2.image, bg2.rect)
    else:
        screen.blit(bg3.image, bg3.rect)
    text_surface, rect = font.render(f"Score: {score}", RED)
    screen.blit(text_surface, (10, 10))

    barriers.draw(screen)
    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
