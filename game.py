import random
import pygame
import pygame.freetype
from tkinter import messagebox

score = 0


class Car(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Draw the car (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Instead we could load a proper pciture of a car...
        self.image = pygame.image.load("car.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels
        self.rect.y = max(0, min(self.rect.y, 500))

    def move_down(self, pixels):
        self.rect.y += pixels
        self.rect.y = max(0, min(self.rect.y, 500-self.image.get_height()))


class Barrier(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Draw the car (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Instead we could load a proper pciture of a car...
        self.image = pygame.image.load("barrier.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def height(self):
        return self.image.get_height()


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
pygame.display.set_caption("Car Racing")

# This will be a list that will contain all the sprites we intend to use in our game.
barriers = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()

playerCar = Car(RED, 0, 0)
playerCar.rect.x = 0
playerCar.rect.y = 230

barrier = Barrier(RED, 0, 0)
barrier.rect.x = 400
barrier.rect.y = 230


# Add the car to the list of objects
player.add(playerCar)
barriers.add(barrier)

# Allowing the user to close the window...
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

    # Game Logic
    if playerCar.rect.colliderect(barrier):
        messagebox.showinfo("Info", "You died!")
        pygame.quit()
    else:
        barrier.rect.x -= 2
        if barrier.rect.x < 0:
            barriers.remove(barrier)
            barrier = Barrier(RED, 0, 0)
            barrier.rect.x = 400
            barrier.rect.y = random.randint(0, 500 - barrier.height())
            barriers.add(barrier)
            score += 1

        barriers.update()

    # Drawing on Screen
    screen.fill(GREEN)

    text_surface, rect = font.render(f"Score: {score}", (0, 0, 0))
    screen.blit(text_surface, (10, 10))
    # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
    barriers.draw(screen)
    player.draw(screen)

    # Refresh Screen
    pygame.display.flip()

    # Number of frames per secong e.g. 60
    clock.tick(60)

pygame.quit()
