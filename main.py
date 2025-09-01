import pygame
import sys
import time

# Inisialisasi
pygame.init()

# Saiz window
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 5, 5
TILE_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DakFarm 2009 Demo - Tanam & Tuai")

# Warna
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 24)

# Grid kebun
EMPTY, SEED, GROWN = 0, 1, 2
field = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
plant_time = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Coin
coins = 0

def draw_field():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            state = field[row][col]
            
            if state == EMPTY:
                pygame.draw.rect(screen, BROWN, rect)
            elif state == SEED:
                pygame.draw.rect(screen, GREEN, rect)
            elif state == GROWN:
                pygame.draw.rect(screen, YELLOW, rect)
            
            pygame.draw.rect(screen, BLACK, rect, 2)  # border

def draw_ui():
    coin_text = font.render(f"Coins: {coins}", True, WHITE)
    screen.blit(coin_text, (10, 10))

def main():
    global coins
    clock = pygame.time.Clock()
    
    while True:
        screen.fill((0, 100, 0))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // TILE_SIZE, y // TILE_SIZE
                
                if row < ROWS and col < COLS:
                    if field[row][col] == EMPTY:
                        field[row][col] = SEED
                        plant_time[row][col] = time.time()
                    elif field[row][col] == GROWN:
                        field[row][col] = EMPTY
                        coins += 10
        
        # Update growth
        for r in range(ROWS):
            for c in range(COLS):
                if field[r][c] == SEED and time.time() - plant_time[r][c] > 5:
                    field[r][c] = GROWN
        
        # Draw
        draw_field()
        draw_ui()
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
