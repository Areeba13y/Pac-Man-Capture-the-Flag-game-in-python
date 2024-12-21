import pygame
import random
import tkinter as tk
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Screen dimensions and grid settings
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create screen
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Capture the Flag")
clock = pygame.time.Clock()

# Game objects
class PacMan:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.score = 0

    def move(self, dx, dy):
        self.x = (self.x + dx * GRID_SIZE) % WIDTH
        self.y = (self.y + dy * GRID_SIZE) % HEIGHT

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 2)


class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move_towards(self, target_x, target_y):
        if self.x < target_x:
            self.x += GRID_SIZE
        elif self.x > target_x:
            self.x -= GRID_SIZE
        if self.y < target_y:
            self.y += GRID_SIZE
        elif self.y > target_y:
            self.y -= GRID_SIZE

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, GRID_SIZE, GRID_SIZE))


# Function to start the game
def start_game():
    # Food items
    food_positions = [
        (random.randint(0, COLS - 1) * GRID_SIZE, random.randint(0, ROWS - 1) * GRID_SIZE)
        for _ in range(20)
    ]

    # Initialize Pac-Men and Ghosts
    pacman_blue = PacMan(GRID_SIZE, GRID_SIZE, BLUE)
    pacman_red = PacMan(WIDTH - GRID_SIZE * 2, HEIGHT - GRID_SIZE * 2, RED)
    ghost_blue = Ghost(GRID_SIZE * 2, GRID_SIZE * 2, BLUE)
    ghost_red = Ghost(WIDTH - GRID_SIZE * 3, HEIGHT - GRID_SIZE * 3, RED)

    # Main game loop
    run = True
    while run:
        clock.tick(10)
        win.fill(BLACK)

        # Draw dividing line
        pygame.draw.line(win, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Draw food
        for pos in food_positions:
            pygame.draw.circle(
                win,
                YELLOW,
                (pos[0] + GRID_SIZE // 2, pos[1] + GRID_SIZE // 2),
                GRID_SIZE // 4,
            )

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Move Pac-Men
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pacman_blue.move(0, -1)
        if keys[pygame.K_s]:
            pacman_blue.move(0, 1)
        if keys[pygame.K_a]:
            pacman_blue.move(-1, 0)
        if keys[pygame.K_d]:
            pacman_blue.move(1, 0)
        if keys[pygame.K_UP]:
            pacman_red.move(0, -1)
        if keys[pygame.K_DOWN]:
            pacman_red.move(0, 1)
        if keys[pygame.K_LEFT]:
            pacman_red.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            pacman_red.move(1, 0)

        # Move ghosts towards opposite Pac-Man
        ghost_blue.move_towards(pacman_red.x, pacman_red.y)
        ghost_red.move_towards(pacman_blue.x, pacman_blue.y)

        # Check for food collection
        new_food_positions = []
        for pos in food_positions:
            if (pacman_blue.x, pacman_blue.y) == pos:
                pacman_blue.score += 1
            elif (pacman_red.x, pacman_red.y) == pos:
                pacman_red.score += 1
            else:
                new_food_positions.append(pos)
        food_positions = new_food_positions

        # Draw Pac-Men and Ghosts
        pacman_blue.draw()
        pacman_red.draw()
        ghost_blue.draw()
        ghost_red.draw()

        # Display scores
        font = pygame.font.SysFont(None, 24)
        score_text_blue = font.render(f"Blue Score: {pacman_blue.score}", True, BLUE)
        score_text_red = font.render(f"Red Score: {pacman_red.score}", True, RED)
        win.blit(score_text_blue, (10, 10))
        win.blit(score_text_red, (WIDTH - 150, 10))

        # Check for collision with ghosts
        if (pacman_blue.x, pacman_blue.y) == (ghost_red.x, ghost_red.y):
            messagebox.showinfo("Game Over", "Red Ghost caught Blue Pac-Man!")
            run = False
        if (pacman_red.x, pacman_red.y) == (ghost_blue.x, ghost_blue.y):
            messagebox.showinfo("Game Over", "Blue Ghost caught Red Pac-Man!")
            run = False

        pygame.display.flip()

    pygame.quit()


# Tkinter GUI
def show_gui():
    root = tk.Tk()
    root.title("Pac-Man Capture the Flag")
    root.geometry("400x200")

    label = tk.Label(
        root, text="Welcome to Pac-Man Capture the Flag!", font=("Arial", 16)
    )
    label.pack(pady=20)

    start_button = tk.Button(
        root,
        text="Start Game",
        font=("Arial", 14),
        bg="green",
        fg="white",
        command=lambda: [root.destroy(), start_game()],
    )
    start_button.pack(pady=10)

    exit_button = tk.Button(
        root,
        text="Exit",
        font=("Arial", 14),
        bg="red",
        fg="white",
        command=root.destroy,
    )
    exit_button.pack(pady=10)

    root.mainloop()


# Start the Tkinter GUI
show_gui()
