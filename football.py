import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Football Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game settings
ball_radius = 15
player_width, player_height = 50, 60
goal_width, goal_height = 20, 200
ball_speed = 4

# Load images
ball_img = pygame.image.load("ball.png")
ball_img = pygame.transform.scale(ball_img, (ball_radius*2, ball_radius*2))
player1_img = pygame.image.load("player1.png")
player1_img = pygame.transform.scale(player1_img, (player_width, player_height))
player2_img = pygame.image.load("player2.png")
player2_img = pygame.transform.scale(player2_img, (player_width, player_height))

# Player and Ball classes
class Player:
    def __init__(self, x, y, img, color):
        self.x = x
        self.y = y
        self.img = img
        self.color = color
        self.rect = self.img.get_rect(topleft=(x, y))
        self.shoot_cooldown = 0

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30
            return Ball(self.x + player_width, self.y + player_height // 2, ball_speed, self.color)

class Ball:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.color = color
        self.dx = speed if color == RED else -speed
        self.dy = random.randint(-5, 5)
        self.radius = 10
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

        # Bounce off all four walls
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.dy = -self.dy
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.dx = -self.dx

# Players and ball
player1 = Player(50, height//2 - player_height//2, player1_img, RED)
player2 = Player(width - 100, height//2 - player_height//2, player2_img, BLUE)
ball = Ball(width//2, height//2, ball_speed, WHITE)

# Goals
goal1 = pygame.Rect(0, (height - goal_height) // 2, goal_width, goal_height)
goal2 = pygame.Rect(width - goal_width, (height - goal_height) // 2, goal_width, goal_height)

# Main game loop
running = True
clock = pygame.time.Clock()
score1 = 0
score2 = 0
ball_in_play = False  # Flag to track if the ball is in play

def display_score():
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Player 1: {score1}  Player 2: {score2}", True, WHITE)
    win.blit(text, (10, 10))

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.y - 5 > 0:
        player1.move(0, -5)
    if keys[pygame.K_s] and player1.y + player_height + 5 < height:
        player1.move(0, 5)
    if keys[pygame.K_UP] and player2.y - 5 > 0:
        player2.move(0, -5)
    if keys[pygame.K_DOWN] and player2.y + player_height + 5 < height:
        player2.move(0, 5)

    if keys[pygame.K_SPACE] and not ball_in_play:
        ball_in_play = True

    if player1.shoot_cooldown > 0:
        player1.shoot_cooldown -= 1

    if ball_in_play:
        ball.move()

        # Check for collisions with players
        if player1.rect.colliderect(ball.rect) or player2.rect.colliderect(ball.rect):
            ball.dx = -ball.dx

        # Check for goals
        if ball.rect.colliderect(goal1):
            print("Player 2 scores!")
            score2 += 1
            ball_in_play = False  # Reset flag
            ball = Ball(width//2, height//2, ball_speed, WHITE)  # Respawn ball at center
        elif ball.rect.colliderect(goal2):
            print("Player 1 scores!")
            score1 += 1
            ball_in_play = False  # Reset flag
            ball = Ball(width//2, height//2, ball_speed, WHITE)  # Respawn ball at center

    # Draw everything
    win.fill(GREEN)
    pygame.draw.rect(win, WHITE, goal1, 2)
    pygame.draw.rect(win, WHITE, goal2, 2)
    player1.draw(win)
    player2.draw(win)
    if ball_in_play:
        ball.draw(win)
    display_score()
    pygame.display.update()

pygame.quit()
