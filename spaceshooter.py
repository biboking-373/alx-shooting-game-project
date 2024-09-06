import pygame
from pygame.locals import *
import sys
import random

# Initialize Pygame
pygame.init()

# Define colors and constants
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FPS = 45
fpslimit = pygame.time.Clock()

# Screen dimensions
sclength = 600
scwidth = 1000
screen = pygame.display.set_mode((scwidth, sclength))
pygame.display.set_caption("Spaceship Game")

# Load background images for each level
backgrounds = {
    "easy": pygame.transform.scale(pygame.image.load("1.jpg"), (scwidth, sclength)),
    "medium": pygame.transform.scale(pygame.image.load("2.jpg"), (scwidth, sclength)),
    "hard": pygame.transform.scale(pygame.image.load("3.jpg"), (scwidth, sclength))
}

# Game variables
level = "easy"  # Starting level
enemy_count = 15  # Number of enemies to start with

# Game running state
isrunning = True

# Define the Bullet class for both player and enemy bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color, direction):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7 * direction  # Direction: -1 for player, 1 for enemy

    def update(self):
        self.rect.y += self.speed
        if self.rect.top < 0 or self.rect.bottom > sclength:
            self.kill()  # Remove the bullet when it goes off the screen

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (scwidth // 2, sclength - 50)  # Position the player at the bottom center of the screen
        self.speed = 5
        self.shoot_delay = 300  # Time delay between bullets (in milliseconds)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed
        if keys[K_UP] or keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_DOWN] or keys[K_s]:
            self.rect.y += self.speed

        # Keep the player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > scwidth:
            self.rect.right = scwidth
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > sclength:
            self.rect.bottom = sclength

    def shoot(self):
        # Shooting green bullets from the player's spaceship
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, GREEN, -1)
            all_sprites.add(bullet)
            player_bullets.add(bullet)

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("DurrrSpaceShip.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, scwidth - 50), random.randint(-100, -40))  # Random starting position
        self.speed = random.randint(1, 5)
        self.shoot_delay = random.randint(500, 1500)  # Time delay between enemy bullets
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed  # Enemy moves down

        # Shoot red bullets
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom, RED, 1)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

        # Reset the enemy position when it goes off the screen
        if self.rect.top > sclength:
            self.rect.center = (random.randint(50, scwidth - 50), random.randint(-100, -40))

# Function to handle game over
def game_over():
    font = pygame.font.SysFont(None, 74)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (scwidth // 2 - 150, sclength // 2 - 50))
    pygame.display.update()
    pygame.time.wait(2000)

    # Restart or exit
    restart_game()

def restart_game():
    global isrunning
    font = pygame.font.SysFont(None, 50)
    text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(text, (scwidth // 2 - 250, sclength // 2 + 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Function to increase the level
def increase_level():
    global level, enemy_count

    if level == "easy":
        level = "medium"
        enemy_count = 30  # Increase enemy count for medium
    elif level == "medium":
        level = "hard"
        enemy_count = 50  # Increase enemy count for hard

# Main function to run the game loop
def main():
    global isrunning, level, enemy_count

    # Instantiate player
    player_one = Player()

    # Create sprite groups
    global all_sprites, player_bullets, enemy_bullets, enemies
    all_sprites = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Add player to the group
    all_sprites.add(player_one)

    # Spawn initial enemies based on the current level
    for _ in range(enemy_count):
        enemy_ship = Enemy()
        all_sprites.add(enemy_ship)
        enemies.add(enemy_ship)

    # Game loop
    isrunning = True
    while isrunning:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Check player input for shooting
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            player_one.shoot()

        # Update all sprites
        all_sprites.update()

        # Check for collisions between player and enemy ships
        if pygame.sprite.spritecollide(player_one, enemies, False):
            game_over()

        # Check for collisions between bullets and ships
        for bullet in player_bullets:
            enemy_hit = pygame.sprite.spritecollideany(bullet, enemies)
            if enemy_hit:
                enemy_hit.kill()
                bullet.kill()

                # Check if all enemies are destroyed
                if len(enemies) == 0:
                    increase_level()  # Go to the next level

                    # Spawn new enemies for the next level
                    for _ in range(enemy_count):
                        enemy_ship = Enemy()
                        all_sprites.add(enemy_ship)
                        enemies.add(enemy_ship)

        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(bullet, player_one):
                game_over()

        # Clear the screen and draw the appropriate background for the level
        screen.blit(backgrounds[level], (0, 0))

        # Draw all sprites
        all_sprites.draw(screen)

        # Update the display
        pygame.display.update()

        # Cap the frame rate
        fpslimit.tick(FPS)

# Run the game
if __name__ == "__main__":
    main()