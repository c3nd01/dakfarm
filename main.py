import pygame
import sys
import os
from config import *

pygame.init()

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DakFarm 8-bit")
clock = pygame.time.Clock()

# Load assets helper
def load_image(path):
    return pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))

# Load tiles
tiles = {
    "grass": load_image("assets/tiles/grass.png"),
    "soil": load_image("assets/tiles/soil.png"),
    "water": load_image("assets/tiles/water.png"),
    "house": load_image("assets/tiles/house.png"),
}

# Load player
player_sprites = {
    "down": load_image("assets/player/down.png"),
    "up": load_image("assets/player/up.png"),
    "left": load_image("assets/player/left.png"),
    "right": load_image("assets/player/right.png"),
}
player_pos = [5, 5]
player_dir = "down"

# Load crops
crops = {
    0: load_image("assets/crops/seed.png"),
    1: load_image("assets/crops/sprout.png"),
    2: load_image("assets/crops/mature.png"),
}
planted = {}  # {(x,y): [stage, time]}

# Load animals
animals = [
    {"type": "cow", "pos": (8, 8), "img": load_image("assets/animals/cow.png")},
    {"type": "chicken", "pos": (10, 10), "img": load_image("assets/animals/chicken.png")},
]

# Map layout
world_map = [
    ["grass"] * 20 for _ in range(15)
]
world_map[7][7] = "house"
world_map[5][5] = "soil"
world_map[5][6] = "soil"
world_map[6][5] = "soil"

inventory = {"crops": 0, "gold": 0}

# Draw map
def draw_world():
    for y, row in enumerate(world_map):
        for x, tile in enumerate(row):
            screen.blit(tiles[tile], (x * TILE_SIZE, y * TILE_SIZE))

    for pos, data in planted.items():
        x, y = pos
        stage = data[0]
        screen.blit(crops[stage], (x * TILE_SIZE, y * TILE_SIZE))

    for animal in animals:
        x, y = animal["pos"]
        screen.blit(animal["img"], (x * TILE_SIZE, y * TILE_SIZE))

# Update crops
def update_crops():
    now = pygame.time.get_ticks() // 1000
    for pos, data in planted.items():
        stage, planted_time = data
        if stage < 2:
            if now - planted_time > CROP_GROWTH_TIME[stage]:
                planted[pos][0] += 1

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))
    draw_world()
    screen.blit(player_sprites[player_dir], (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Gold: {inventory['gold']} | Crops: {inventory['crops']}", True, (255,255,255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

    update_crops()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_pos[1] -= 1
                player_dir = "up"
            elif event.key == pygame.K_DOWN:
                player_pos[1] += 1
                player_dir = "down"
            elif event.key == pygame.K_LEFT:
                player_pos[0] -= 1
                player_dir = "left"
            elif event.key == pygame.K_RIGHT:
                player_pos[0] += 1
                player_dir = "right"
            elif event.key == pygame.K_SPACE:
                pos = (player_pos[0], player_pos[1])
                if world_map[pos[1]][pos[0]] == "soil":
                    if pos not in planted:
                        planted[pos] = [0, pygame.time.get_ticks() // 1000]
            elif event.key == pygame.K_RETURN:
                pos = (player_pos[0], player_pos[1])
                if pos in planted and planted[pos][0] == 2:
                    inventory["crops"] += 1
                    del planted[pos]
            elif event.key == pygame.K_s:
                if inventory["crops"] > 0:
                    inventory["gold"] += inventory["crops"] * 5
                    inventory["crops"] = 0
