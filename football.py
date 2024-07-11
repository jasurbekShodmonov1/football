import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1000, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Football Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game settings
ball_radius = 10
player_width, player_height = 20, 80
goal_width, goal_height = 20, 160
ball_speed = 3

# Load images (if you have specific player and ball images, load them here)
ball_img = pygame.image.load("ball.png")
ball_img = pygame.transform.scale(ball_img, (ball_radius * 2, ball_radius * 2))


# Player and Ball classes (using basic colored rectangles for players)
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = player_width
        self.height = player_height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shoot_cooldown = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def move_to_center(self, center_x, center_y):
        # Move player towards the center horizontally
        if self.x < center_x:
            self.move(5, 0)
        elif self.x > center_x:
            self.move(-5, 0)

        # Move player towards the center vertically once horizontal movement is complete
        if self.x == center_x:
            if self.y < center_y:
                self.move(0, 5)
            elif self.y > center_y:
                self.move(0, -5)

        # Check if player has reached center
        if self.x == center_x and self.y == center_y:
            self.move_to_center = False

    def move_up(self):
        if self.y > 0:
            self.move(0, -5)

    def move_down(self):
        if self.y < height - self.height:
            self.move(0, 5)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30
            return Ball(self.x + self.width, self.y + self.height // 2, ball_speed)


class Ball:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.color = WHITE
        self.dx = speed if random.randint(0, 1) == 0 else -speed
        self.dy = random.randint(-5, 5)
        self.radius = ball_radius
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

        # Bounce off walls
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.dy = -self.dy
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.dx = -self.dx


# Players and ball
player1 = Player(100, height // 2 - player_height // 2, RED)
player2 = Player(width - 100 - player_width, height // 2 - player_height // 2, BLUE)

# Move players towards the center
center_x, center_y = width // 2, height // 2
player1.move_to_center(center_x, center_y)
player2.move_to_center(center_x, center_y)

ball = Ball(width // 2, height // 2, ball_speed)  # Initialize ball towards center

# Goals
goal1 = pygame.Rect(0, (height - goal_height) // 2, goal_width, goal_height)
goal2 = pygame.Rect(width - goal_width, (height - goal_height) // 2, goal_width, goal_height)

# Center circle
center_circle_radius = 100
center_circle = pygame.Rect(width // 2 - center_circle_radius, height // 2 - center_circle_radius,
                            center_circle_radius * 2, center_circle_radius * 2)

# Penalty areas
penalty_width, penalty_height = 160, 400
penalty1 = pygame.Rect(0, (height - penalty_height) // 2, penalty_width, penalty_height)
penalty2 = pygame.Rect(width - penalty_width, (height - penalty_height) // 2, penalty_width, penalty_height)

# Halfway line
halfway_line = pygame.Rect(width // 2 - 2, 0, 4, height)

# Penalty spots
penalty_spot_radius = 5
penalty_spot1 = (penalty_width, height // 2)
penalty_spot2 = (width - penalty_width, height // 2)

# Font for timer display
pygame.font.init()
font = pygame.font.Font(None, 36)

# Countdown timer settings
game_duration = 90  # 90 seconds
start_time = 0
elapsed_time = 0
match_ended = False

# Function to display score and timer
def display_score_and_timer():
    text_score = font.render(f"Player 1: {score1}  Player 2: {score2}", True, WHITE)
    win.blit(text_score, (10, 10))

    # Calculate remaining time
    if not match_ended:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000
        remaining_time = max(0, game_duration - elapsed_time)

        text_timer = font.render(f"Time left: {remaining_time} seconds", True, WHITE)
        win.blit(text_timer, (width - text_timer.get_width() - 10, 10))
    else:
        if score1 > score2:
            text_winner = font.render(f"Player 1 wins! 🏆", True, WHITE)
        elif score2 > score1:
            text_winner = font.render(f"Player 2 wins! 🏆", True, WHITE)
        else:
            text_winner = font.render(f"Draw!", True, WHITE)

        win.blit(text_winner, (width // 2 - text_winner.get_width() // 2, height // 2 - text_winner.get_height() // 2))


# Main game loop
running = True
clock = pygame.time.Clock()
score1 = 0
score2 = 0
ball_in_play = False

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player1.x - 5 > 0:
        player1.move(-5, 0)
    if keys[pygame.K_d] and player1.x + player_width + 5 < width:
        player1.move(5, 0)
    if keys[pygame.K_w]:
        player1.move_up()
    if keys[pygame.K_s]:
        player1.move_down()

    if keys[pygame.K_LEFT] and player2.x - 5 > 0:
        player2.move(-5, 0)
    if keys[pygame.K_RIGHT] and player2.x + player_width + 5 < width:
        player2.move(5, 0)
    if keys[pygame.K_UP]:
        player2.move_up()
    if keys[pygame.K_DOWN]:
        player2.move_down()

    if keys[pygame.K_SPACE] and not ball_in_play and not match_ended:
        ball_in_play = True
        start_time = pygame.time.get_ticks()

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
            ball_in_play = False
            ball = Ball(width // 2, height // 2, ball_speed)
            match_ended = True
        elif ball.rect.colliderect(goal2):
            print("Player 1 scores!")
            score1 += 1
            ball_in_play = False
            ball = Ball(width // 2, height // 2, ball_speed)
            match_ended = True

        # Check if time is up
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000
        if elapsed_time >= game_duration:
            match_ended = True

    # Draw everything
    win.fill(GREEN)

    # Draw center circle
    pygame.draw.circle(win, WHITE, center_circle.center, center_circle_radius, width=2)

    # Draw penalty areas
    pygame.draw.rect(win, WHITE, penalty1, width=2)
    pygame.draw.rect(win, WHITE, penalty2, width=2)

    # Draw penalty spots
    pygame.draw.circle(win, WHITE, penalty_spot1, penalty_spot_radius)
    pygame.draw.circle(win, WHITE, penalty_spot2, penalty_spot_radius)

    # Draw halfway line
    pygame.draw.rect(win, WHITE, halfway_line)

    # Draw goals
    pygame.draw.rect(win, WHITE, goal1, width=2)
    pygame.draw.rect(win, WHITE, goal2, width=2)

    # Draw players and ball
    player1.draw(win)
    player2.draw(win)
    if ball_in_play:
        ball.draw(win)

    # Display score and timer
    display_score_and_timer()

    pygame.display.update()

pygame.quit()
