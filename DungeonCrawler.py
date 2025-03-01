'''
    File name: DungeonCrawler.py
    Author: Onur Ishak Bulut
    Date created: 10/01/2025
    Date last modified: 27/01/2025
    Python Version: 3.3
'''
import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
TILE_SIZE = 32
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
POTION_WEIGHTS = {
    "small": 60,
    "medium": 30,
    "large": 10
}

# Scaling Factors
BASE_ENEMY_HEALTH_MULTIPLIER = 1
BASE_ENEMY_DAMAGE_INCREMENT = 1
MIN_ENEMY_DAMAGE = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rogue-like Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

FONT_PATH = "MinimalPixelFont.ttf"

# Player animation states
player_animation_state = "idle"  # "idle", "attacking", "damaged"
player_current_frame = 0
player_frame_counter = 0
player_direction = "right"

# Game state
game_state = "player_turn"

# Player progression
player_xp = 0
player_level = 1
xp_for_next_level = 10
current_level = 1
stat_points = 0

# Player Stats
strength = 1
vitality = 1

# Log
log = []

# Visibility
visibility = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Base Enemy Types
ENEMY_TYPES = {
    "goblin": {"health": 10, "damage": 3, "speed": 1, "color": RED},
    "slime": {"health": 5, "damage": 5, "speed": 1, "color": BLUE},
    "warg": {"health": 100, "damage": 15, "speed": 2, "color": (128, 0, 128)}
}

# Load sprites
player_sprite = pygame.image.load("frame1.png").convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (96, 96))
attack_right_sprites = [
    pygame.transform.scale(pygame.image.load(
        f"./playerattackr/attackright{i}.png")
                           .convert_alpha(), (96, 96))
    for i in range(1, 5)
]

# Load player damage animation frames
player_damage_frames = [
    pygame.transform.scale(pygame.image.load(
        f"./playerdmg/playerdmg{i}.png").
                           convert_alpha(), (96, 96))
    for i in range(1, 5)
]

# Load empty armor sprites
empty_helmet = pygame.image.load("emptyarmor/emptyhelmet.png").convert_alpha()
empty_chestplate = (pygame.image.load
                    ("emptyarmor/emptychestplate.png").convert_alpha())
empty_leggings = (pygame.image.load
                  ("emptyarmor/emptylegings.png").convert_alpha())
empty_boots = pygame.image.load("emptyarmor/emptyboots.png").convert_alpha()

# Scale the sprites to fit the UI
empty_helmet = pygame.transform.scale(empty_helmet, (32, 32))
empty_chestplate = pygame.transform.scale(empty_chestplate, (32, 32))
empty_leggings = pygame.transform.scale(empty_leggings, (32, 32))
empty_boots = pygame.transform.scale(empty_boots, (32, 32))

# Wall tileset
wall_tileset = pygame.image.load(f"wall4bit.png").convert_alpha()
wall_tileset = pygame.transform.scale(wall_tileset, (TILE_SIZE, TILE_SIZE))

# Floor tileset
floor_tileset = pygame.image.load("tileset/floor1.png").convert_alpha()
floor_tileset = pygame.transform.scale(floor_tileset, (TILE_SIZE, TILE_SIZE))

# Chest sprites
closed_chest = (pygame.image.load
                ("tileset/chest/clossedchest.png").convert_alpha())
closed_chest = pygame.transform.scale(closed_chest, (TILE_SIZE, TILE_SIZE))
open_chest = pygame.image.load("tileset/chest/openchest.png").convert_alpha()
open_chest = pygame.transform.scale(open_chest, (TILE_SIZE, TILE_SIZE))

# Stair sprite
stair_tileset = pygame.image.load("tileset/floor_stairs.png").convert_alpha()
stair_tileset = pygame.transform.scale(stair_tileset, (TILE_SIZE, TILE_SIZE))

# Enemy sprites
goblin_sprite = pygame.image.load("enemies/Goblin1.png").convert_alpha()
goblin_sprite = pygame.transform.scale(goblin_sprite, (96, 96))
goblin_attack_sprites = [
    pygame.transform.scale(pygame.image.load
                           (f"./goblinattack/goblinattack{i}.png")
                           .convert_alpha(), (96, 96))
    for i in range(1, 5)
]

slime_sprite = pygame.image.load("enemies/Slime1.png").convert_alpha()
slime_sprite = pygame.transform.scale(slime_sprite, (96, 96))
slime_attack_sprites = [
    pygame.transform.scale(pygame.image.load
                           (f"./slimeattack/slimeattack{i}.png")
                           .convert_alpha(), (96, 96))
    for i in range(1, 5)
]

# Death animations
slime_death_frames = [
    pygame.transform.scale(pygame.image.load
                           (f"./slimedead/slimedie{i}.png")
                           .convert_alpha(), (96, 96))
    for i in range(1, 10)
]

goblin_death_frames = [
    pygame.transform.scale(pygame.image.load
                           (f"./goblindead/goblindie{i}.png")
                           .convert_alpha(), (96, 96))
    for i in range(1, 13)
]

# Loading goblin damage animation frames
goblin_damage_frames = [
    pygame.transform.scale(pygame.image.load
                           (f"./goblindmg/goblindmg{i}.png")
                           .convert_alpha(), (96, 96))
    for i in range(1, 5)
]

# Loading Warg sprites
warg_sprite = pygame.image.load("enemies/warg.png").convert_alpha()
warg_sprite = pygame.transform.scale(warg_sprite, (96, 96))

warg_attack_sprites = [
    pygame.transform.scale(pygame.image.load(f"./wargattack"
                                             f"/wargattack{i}.png")
                           .convert_alpha(), (96, 96))
    for i in range(1, 5)
]

warg_damage_frames = [
    pygame.transform.scale(pygame.image.load(f"./wargdamage/"
                                             f"wargdamage{i}.png")
                           .convert_alpha(), (96, 96))
    for i in range(1, 5)
]

# Potion sprites
small_potion_sprite = (pygame.image.load
                       ("potions/smallpotion.png").convert_alpha())
small_potion_sprite = (pygame.transform.scale
                       (small_potion_sprite, (TILE_SIZE, TILE_SIZE)))
medium_potion_sprite = (pygame.image.load
                        ("potions/mediumpotion.png").convert_alpha())
medium_potion_sprite = (pygame.transform.scale
                        (medium_potion_sprite, (TILE_SIZE, TILE_SIZE)))
large_potion_sprite = (pygame.image.load
                       ("potions/largepotion.png").convert_alpha())
large_potion_sprite = (pygame.transform.scale
                       (large_potion_sprite, (TILE_SIZE, TILE_SIZE)))

potion_sprites = {
    "small": small_potion_sprite,
    "medium": medium_potion_sprite,
    "large": large_potion_sprite,
}

# Sprite offset
SPRITE_OFFSET_X = (96 - TILE_SIZE) // 2
SPRITE_OFFSET_Y = (96 - TILE_SIZE) // 2


# Dungeon Generator
class Map:
    def __init__(self):
        self.mapArr = []
        self.roomList = []

    def makeMap(self, xsize, ysize, fail, b1, mrooms):
        self.mapArr = [[1 for _ in range(xsize)] for _ in range(ysize)]
        for _ in range(mrooms):
            room_w, room_h = random.randint(3, 15), random.randint(3, 15)
            room_x, room_y = (random.randint
                              (1, xsize - room_w - 1),
                              random.randint(1, ysize - room_h - 1))
            new_room = [room_w, room_h, room_x, room_y]
            if all(not (room_x < r[2] + r[0] and room_x + room_w > r[2] and
                        room_y < r[3] + r[1]
                        and room_y + room_h > r[3]) for r in self.roomList):
                self.roomList.append(new_room)
                for x in range(room_x, room_x + room_w):
                    for y in range(room_y, room_y + room_h):
                        self.mapArr[y][x] = 0

        for i in range(len(self.roomList) - 1):
            x1, y1 = (self.roomList[i][2] + self.roomList[i][0]
                      // 2, self.roomList[i][3] + self.roomList[i][1] // 2)
            x2, y2 = (self.roomList[i + 1][2] +
                      self.roomList[i + 1][0] // 2,
                      self.roomList[i + 1][3] +
                      self.roomList[i + 1][1] // 2)
            self.create_corridor(x1, y1, x2, y2)

        last_room = self.roomList[-1]
        self.staircase_pos = (last_room[2] +
                              last_room[0] // 2,
                              last_room[3] + last_room[1] // 2)
        self.mapArr[self.staircase_pos[1]][self.staircase_pos[0]] = 2

    def create_corridor(self, x1, y1, x2, y2):
        if random.choice([True, False]):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.mapArr[y1][x] = 0
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.mapArr[y][x2] = 0
        else:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.mapArr[y][x1] = 0
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.mapArr[y2][x] = 0


# Armor class
class Armor:
    def __init__(self, name, armor_type, sprite):
        self.name = name
        self.armor_type = armor_type
        self.sprite = sprite


# Game initialization
themap = Map()
themap.makeMap(GRID_WIDTH, GRID_HEIGHT, fail=50, b1=50, mrooms=50)
map_data = themap.mapArr
staircase_pos = themap.staircase_pos
first_room = themap.roomList[0]
player_pos = [first_room[2] + first_room[0]
              // 2, first_room[3] +
              first_room[1] // 2]


# Fog of war
def reveal_area(x, y):
    for dy in range(-5, 6):
        for dx in range(-5, 6):
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                visibility[ny][nx] = True


reveal_area(player_pos[0], player_pos[1])


# Game over screen initialization
def game_over_screen():
    replay_button = (pygame.image.load
                     ("buttons/restartbutton.png").convert_alpha())
    quit_button = (pygame.image.load
                   ("buttons/quitbutton.png").convert_alpha())

    # Resize buttons
    button_width, button_height = 180, 50
    replay_button = (pygame.transform.scale
                     (replay_button, (button_width, button_height)))
    quit_button = pygame.transform.scale(quit_button,
                                         (button_width, button_height))

    # Button positions
    replay_button_rect = replay_button.get_rect(center=(SCREEN_WIDTH //
                                                        2, SCREEN_HEIGHT //
                                                        2 + 50))
    quit_button_rect = quit_button.get_rect(center=(SCREEN_WIDTH //
                                                    2, SCREEN_HEIGHT //
                                                    2 + 150))

    # Title font
    title_font = pygame.font.Font(FONT_PATH, 72)
    title_text = title_font.render("You're Dead!", True, RED)

    while True:
        screen.fill(BLACK)

        # Draw title
        screen.blit(title_text, (SCREEN_WIDTH // 2
                                 - title_text.get_width() //
                                 2, 100))

        # Draw buttons
        screen.blit(replay_button, replay_button_rect)
        screen.blit(quit_button, quit_button_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if replay_button_rect.collidepoint(mouse_pos):
                    restart_game()
                    return  # Return to the main game loop
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(15)


def move_enemies():
    global player_hp, player_animation_state, \
        player_current_frame, player_frame_counter

    for enemy in enemies:
        if enemy.get('animation_state') in ['dying', 'attacking']:
            continue

        dx = player_pos[0] - enemy["x"]
        dy = player_pos[1] - enemy["y"]
        enemy["facing"] = "right" if dx > 0 else "left"

        if abs(dx) + abs(dy) == 1:
            enemy["animation_state"] = "attacking"
            enemy["current_frame"] = 0
            enemy["frame_counter"] = 0
            damage = max(1, enemy["damage"] - strength)
            player_hp -= damage
            log.append(f"An {enemy['type']} attacks you for {damage} damage!")

            # Trigging player damage animation
            player_animation_state = "damaged"
            player_current_frame = 0
            player_frame_counter = 0

            if player_hp <= 0:
                log.append("You died!")
                game_over_screen()
                return
        else:
            if abs(dx) > abs(dy):
                new_x = enemy["x"] + (1 if dx > 0 else -1)
                if (0 <= new_x < GRID_WIDTH and
                        map_data[enemy["y"]][new_x] == 0 and not any(
                                            e["x"] == new_x and e["y"]
                                            == enemy["y"] for e in enemies)):
                    enemy["x"] = new_x
            else:
                new_y = enemy["y"] + (1 if dy > 0 else -1)
                if (0 <= new_y < GRID_HEIGHT and
                        map_data[new_y][enemy["x"]] == 0 and not any(
                        e["x"] == enemy["x"] and e["y"]
                        == new_y for e in enemies)):
                    enemy["y"] = new_y


# Checking the level up state
def check_level_up():
    global player_xp, player_level, \
        xp_for_next_level, player_max_hp, \
        player_hp, stat_points
    while player_xp >= xp_for_next_level:
        player_xp -= xp_for_next_level
        player_level += 1
        xp_for_next_level = int(xp_for_next_level * 2)
        stat_points += 1
        player_max_hp += 5
        player_hp += 5
        log.append(f"Level up! Now level "
                   f"{player_level} with {stat_points} stat points!")


# Generating random treasures
def generate_treasures(num_objects):
    corners = []
    for room in themap.roomList:
        room_w, room_h, room_x, room_y = room

        room_corners = [
            (room_x, room_y, 'east'),
            (room_x + room_w - 1, room_y, 'west'),
            (room_x, room_y + room_h - 1, 'east'),
            (room_x + room_w - 1, room_y + room_h - 1, 'west')
        ]

        for x, y, direction in room_corners:
            if (0 <= x < GRID_WIDTH and 0 <= y
                    < GRID_HEIGHT and map_data[y][x] == 0):
                corners.append((x, y, direction))

    selected = random.sample(corners, min(num_objects, len(corners)))
    return [{'x': x, 'y': y, 'state': 'closed',
             'direction': dir} for (x, y, dir) in selected]


# Generating random enemies
def generate_enemies(num_objects):
    empty_tiles = [(x, y) for y in range(GRID_HEIGHT)
                   for x in range(GRID_WIDTH)
                   if map_data[y][x] == 0]
    enemies = []

    # Spawning the warg boss
    if current_level == 3:
        x, y = random.choice(empty_tiles)
        enemies.append({
            "x": x,
            "y": y,
            "type": "warg",
            "animation_state": "alive",
            "current_frame": 0,
            "frame_counter": 0,
            "health": ENEMY_TYPES["warg"]["health"] * 2,
            "damage": ENEMY_TYPES["warg"]["damage"],
            "speed": ENEMY_TYPES["warg"]["speed"],
            "color": ENEMY_TYPES["warg"]["color"],
            "facing": "right"
        })
        empty_tiles.remove((x, y))

    # Spawn regular enemies
    for _ in range(num_objects):
        enemy_type = random.choice(["goblin", "slime"])
        base_stats = ENEMY_TYPES[enemy_type]
        x, y = random.choice(empty_tiles)

        scaled_health = base_stats["health"] * (1 +
                                                (current_level - 1)
                                                * BASE_ENEMY_HEALTH_MULTIPLIER)
        scaled_damage = (base_stats["damage"] +
                         (current_level - 1)
                         * BASE_ENEMY_DAMAGE_INCREMENT)

        enemies.append({
            "x": x,
            "y": y,
            "type": enemy_type,
            "animation_state": "alive",
            "current_frame": 0,
            "frame_counter": 0,
            "health": scaled_health,
            "damage": max(MIN_ENEMY_DAMAGE, scaled_damage),
            "speed": base_stats["speed"],
            "color": base_stats["color"],
            "facing": "right"
        })

    return enemies


# Drawing the warg health bar
def draw_warg_health_bar():
    warg = next((e for e in enemies if e["type"]
                 == "warg" and e["animation_state"]
                 != "dying"), None)
    if warg:
        # Draw health bar
        health_bar_width = 400
        health_bar_height = 20
        health_ratio = warg["health"] / (ENEMY_TYPES["warg"]["health"] * 2)
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2
                                       - health_bar_width // 2, 50,
                                       health_bar_width *
                                       health_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 -
                                         health_bar_width // 2, 50,
                                         health_bar_width,
                                         health_bar_height), 2)

        # Draw Warg sprite above the health bar
        warg_sprite_scaled = pygame.transform.scale(warg_sprite, (64, 64))
        screen.blit(warg_sprite_scaled, (SCREEN_WIDTH // 2 - 32, 10))


treasures = generate_treasures(3)
enemies = generate_enemies(5 + current_level)


# Drawing the randomized map
def draw_map():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if visibility[y][x]:
                if map_data[y][x] == 1:
                    screen.blit(wall_tileset, (x * TILE_SIZE, y * TILE_SIZE))
                elif map_data[y][x] == 2:
                    screen.blit(stair_tileset, (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    screen.blit(floor_tileset, (x * TILE_SIZE, y * TILE_SIZE))
            else:
                pygame.draw.rect(screen, DARK_GRAY,
                                 (x * TILE_SIZE, y * TILE_SIZE,
                                  TILE_SIZE, TILE_SIZE))


# Drawing chest and enemies
def draw_objects():
    global enemies

    # Draw treasures
    for treasure in treasures:
        if visibility[treasure['y']][treasure['x']]:
            if treasure['state'] == 'closed':
                img = pygame.transform.flip(closed_chest,
                                            treasure['direction']
                                            == 'west', False)
            else:
                img = pygame.transform.flip(open_chest,
                                            treasure['direction']
                                            == 'west', False)
            screen.blit(img, (treasure['x'] *
                              TILE_SIZE, treasure['y']
                              * TILE_SIZE))

    # Draw enemies
    for enemy in enemies[:]:
        if visibility[enemy["y"]][enemy["x"]]:
            if enemy["animation_state"] == "dying":
                if enemy["type"] == "slime":
                    frames = slime_death_frames
                elif enemy["type"] == "goblin":
                    frames = goblin_death_frames
                screen.blit(frames[enemy["current_frame"]],
                            (enemy["x"] * TILE_SIZE - SPRITE_OFFSET_X,
                             enemy["y"] * TILE_SIZE - SPRITE_OFFSET_Y))
                enemy["frame_counter"] += 1
                if enemy["frame_counter"] >= 3:
                    enemy["current_frame"] += 1
                    enemy["frame_counter"] = 0
                    if enemy["current_frame"] >= len(frames):
                        enemies.remove(enemy)

            elif enemy["animation_state"] == "attacking":
                if enemy["type"] == "goblin":
                    sprites = goblin_attack_sprites
                elif enemy["type"] == "slime":
                    sprites = slime_attack_sprites
                elif enemy["type"] == "warg":
                    sprites = warg_attack_sprites

                current_sprite = sprites[enemy["current_frame"]]
                if enemy["facing"] == "left":
                    current_sprite = (pygame.transform.flip
                                      (current_sprite, True, False))

                screen.blit(current_sprite, (enemy["x"] *
                                             TILE_SIZE - SPRITE_OFFSET_X,
                                             enemy["y"] *
                                             TILE_SIZE - SPRITE_OFFSET_Y))

                enemy["frame_counter"] += 1
                if enemy["frame_counter"] >= 3:
                    enemy["current_frame"] += 1
                    enemy["frame_counter"] = 0
                    if enemy["current_frame"] >= len(sprites):
                        enemy["animation_state"] = "alive"

            elif enemy["animation_state"] == "damaged":
                if enemy["type"] == "goblin":
                    frames = goblin_damage_frames
                elif enemy["type"] == "warg":
                    frames = warg_damage_frames
                else:
                    frames = []
                if frames:
                    current_sprite = frames[enemy["current_frame"]]
                    if enemy["facing"] == "left":
                        current_sprite = (pygame.transform.flip
                                          (current_sprite, True, False))

                    screen.blit(current_sprite, (enemy["x"] * TILE_SIZE -
                                                 SPRITE_OFFSET_X, enemy["y"] *
                                                 TILE_SIZE - SPRITE_OFFSET_Y))

                    enemy["frame_counter"] += 1
                    if enemy["frame_counter"] >= 3:
                        enemy["current_frame"] += 1
                        enemy["frame_counter"] = 0
                        if enemy["current_frame"] >= len(frames):
                            enemy["animation_state"] = "alive"

            else:
                if enemy["type"] == "goblin":
                    sprite = pygame.transform.flip(
                        goblin_sprite, enemy["facing"] == "left", False)
                elif enemy["type"] == "slime":
                    sprite = pygame.transform.flip(
                        slime_sprite, enemy["facing"] == "left", False)
                elif enemy["type"] == "warg":
                    sprite = pygame.transform.flip(
                        warg_sprite, enemy["facing"] == "left", False)

                screen.blit(sprite, (enemy["x"] * TILE_SIZE -
                                     SPRITE_OFFSET_X, enemy["y"] *
                                     TILE_SIZE - SPRITE_OFFSET_Y))

    # Draw player
    if player_animation_state == "attacking":
        if player_direction == "right":
            current_sprite = attack_right_sprites[player_current_frame]
        elif player_direction == "left":
            current_sprite = (pygame.transform.flip
                              (attack_right_sprites[player_current_frame],
                               True, False))
        else:
            current_sprite = attack_right_sprites[player_current_frame]
    elif player_animation_state == "damaged":
        current_sprite = player_damage_frames[player_current_frame]
        if player_direction == "left":
            current_sprite = pygame.transform.flip(current_sprite, True, False)
    else:
        if player_direction == "left":
            current_sprite = pygame.transform.flip(player_sprite, True, False)
        else:
            current_sprite = player_sprite

    screen.blit(current_sprite, (player_pos[0] *
                                 TILE_SIZE - SPRITE_OFFSET_X,
                                 player_pos[1] * TILE_SIZE - SPRITE_OFFSET_Y))


# Drawing User Interface
def draw_ui():
    pygame.draw.rect(screen, RED, pygame.Rect
                     (10, SCREEN_HEIGHT - 40,
                      (player_hp / player_max_hp) * 200, 20))
    pygame.draw.rect(screen, WHITE, pygame.Rect
                     (10, SCREEN_HEIGHT - 40, 200, 20), 2)
    xp_bar_width = int((player_xp / xp_for_next_level) * 200)
    pygame.draw.rect(screen, GREEN, pygame.Rect
                     (10, SCREEN_HEIGHT - 20, xp_bar_width, 10))
    pygame.draw.rect(screen, WHITE, pygame.Rect
                     (10, SCREEN_HEIGHT - 20, 200, 10), 1)

    level_text = font.render(f"Player: {player_level} "
                             f"| Dungeon: {current_level} | "
                             f"XP: {player_xp}/{xp_for_next_level}",
                             True, WHITE)
    screen.blit(level_text, (10, SCREEN_HEIGHT - 60))

    y_offset = SCREEN_HEIGHT - 80
    for line in log[-3:]:
        text = font.render(line, True, WHITE)
        screen.blit(text, (10, y_offset))
        y_offset -= 20


# Drawing the inventory
def draw_status_window():
    status_surface = pygame.Surface((500, 400))
    status_surface.fill(DARK_GRAY)
    pygame.draw.rect(status_surface, WHITE, status_surface.get_rect(), 2)

    title = font.render("Character Stats & Inventory", True, WHITE)
    status_surface.blit(title, (10, 10))

    stats = [
        f"Health: {player_hp}/{player_max_hp}",
        f"Level: {player_level}",
        f"XP: {player_xp}/{xp_for_next_level}",
        f"Strength: {strength}",
        f"Vitality: {vitality}",
        f"Stat Points: {stat_points}",
    ]

    y_offset = 40
    for stat in stats:
        stat_text = font.render(stat, True, WHITE)
        status_surface.blit(stat_text, (10, y_offset))
        y_offset += 20
    inventory_title = font.render("Inventory:", True, WHITE)
    status_surface.blit(inventory_title, (10, y_offset))
    y_offset += 30

    potion_entries = [
        ("Small Potion", small_potion_sprite),
        ("Medium Potion", medium_potion_sprite),
        ("Large Potion", large_potion_sprite)
    ]

    for potion_name, sprite in potion_entries:
        # Draw potion image
        status_surface.blit(sprite, (10, y_offset - 5))
        # Draw potion text
        count = inventory[potion_name]
        item_text = font.render(f"{potion_name}: {count}", True, WHITE)
        status_surface.blit(item_text, (50, y_offset))
        y_offset += 40

    # Draw armor on the right side
    armor_title = font.render("Armor:", True, WHITE)
    status_surface.blit(armor_title, (250, 40))
    y_offset_armor = 80

    armor_slots = [
        ("Helmet", "helmet", empty_helmet),
        ("Chestplate", "chestplate", empty_chestplate),
        ("Leggings", "leggings", empty_leggings),
        ("Boots", "boots", empty_boots)
    ]

    for slot_name, slot_type, empty_sprite in armor_slots:
        # Draw slot name
        slot_text = font.render(slot_name, True, WHITE)
        status_surface.blit(slot_text, (250, y_offset_armor))

        # Draw armor sprite (empty or equipped)
        if equipped_armor[slot_type]:
            status_surface.blit(equipped_armor
                                [slot_type].sprite,
                                (350, y_offset_armor - 5))
        else:
            status_surface.blit(empty_sprite, (350, y_offset_armor - 5))

        y_offset_armor += 40

    screen.blit(status_surface, (200, 100))


# Drawing the potion menu
def draw_potion_selection():
    selection_surface = pygame.Surface((300, 200))
    selection_surface.fill(DARK_GRAY)
    pygame.draw.rect(selection_surface, WHITE, selection_surface.get_rect(), 2)

    title = font.render("Select Potion:", True, WHITE)
    selection_surface.blit(title, (10, 10))

    y_offset = 40
    potion_list = [
        ("Small Potion", small_potion_sprite, "1"),
        ("Medium Potion", medium_potion_sprite, "2"),
        ("Large Potion", large_potion_sprite, "3")
    ]

    for i, (potion_name, sprite, key) in enumerate(potion_list):
        # Draw key number
        key_text = font.render(f"{key}.", True, WHITE)
        selection_surface.blit(key_text, (10, y_offset))

        # Draw potion image
        selection_surface.blit(sprite, (40, y_offset - 5))

        # Draw potion name and count
        count = inventory[potion_name]
        text = font.render(f"{potion_name} ({count})", True, WHITE)
        selection_surface.blit(text, (80, y_offset))

        y_offset += 50

    screen.blit(selection_surface,
                (SCREEN_WIDTH // 2 - 150,
                 SCREEN_HEIGHT // 2 - 100))


# Generating the new level of the dungeon
def generate_new_level():
    global themap, map_data, player_pos, treasures, \
        enemies, visibility, staircase_pos, current_level
    current_level += 1
    themap = Map()
    themap.makeMap(GRID_WIDTH, GRID_HEIGHT, fail=50, b1=50, mrooms=20)
    map_data = themap.mapArr
    staircase_pos = themap.staircase_pos
    first_room = themap.roomList[0]
    player_pos = [first_room[2] + first_room[0] // 2,
                  first_room[3] + first_room[1] // 2]
    treasures = generate_treasures(5)
    enemies = generate_enemies(5 + current_level)
    visibility = [[False] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    reveal_area(player_pos[0], player_pos[1])
    log.append(f"Descended to dungeon level {current_level}!")
    log.append("Enemies grow stronger!")


# Handling the player inputs
def handle_player_input(event):
    global inventory_open, potion_selection, \
        game_state, player_animation_state, \
        player_current_frame, player_frame_counter, \
        player_direction, player_hp, \
        player_max_hp, player_xp, xp_for_next_level, player_level, \
        stat_points, strength, vitality

    if event.key == pygame.K_i:
        inventory_open = not inventory_open
    elif event.key == pygame.K_s and stat_points > 0:
        strength += 1
        stat_points -= 1
        log.append(f"You increased Strength to {strength}!")
    elif event.key == pygame.K_v and stat_points > 0:
        vitality += 1
        player_max_hp += 5
        player_hp += 5
        stat_points -= 1
        log.append(f"You increased Vitality to {vitality}!")
    elif event.key == pygame.K_e:
        handle_interaction()
    elif event.key == pygame.K_u and not inventory_open:
        if sum(inventory.values()) > 0:
            potion_selection = not potion_selection
        else:
            log.append("No potions in inventory!")
    elif event.key in [pygame.K_1, pygame.K_2,
                       pygame.K_3] and potion_selection:
        handle_potion_use(event.key)
    else:
        handle_movement(event)


# Handling the movement
def handle_movement(event):
    global player_pos, game_state, player_animation_state, \
        player_current_frame, player_frame_counter, player_direction

    dx, dy = 0, 0
    if event.key == pygame.K_UP:
        dy = -1
    elif event.key == pygame.K_DOWN:
        dy = 1
    elif event.key == pygame.K_LEFT:
        dx = -1
    elif event.key == pygame.K_RIGHT:
        dx = 1

    if dx != 0 or dy != 0:
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        handle_player_move(new_x, new_y, dx, dy)


# Handling the player interactions
def handle_player_move(new_x, new_y, dx, dy):
    global player_pos, game_state, player_animation_state, \
        player_current_frame, player_frame_counter, \
        player_direction

    enemy_in_path = next((e for e in enemies if e["x"] ==
                          new_x and e["y"] == new_y and
                          e["animation_state"] != "dying"), None)
    chest_blocking = any(t['x'] == new_x and t['y'] ==
                         new_y and t['state'] == 'closed' for t in treasures)

    if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT
            and map_data[new_y][new_x] in [0, 2] and not chest_blocking):
        if enemy_in_path:
            handle_attack(enemy_in_path, dx, dy)
        else:
            player_pos[0] = new_x
            player_pos[1] = new_y
            reveal_area(player_pos[0], player_pos[1])
            game_state = "enemy_turn"


# Attack state Handler
def handle_attack(enemy, dx, dy):
    global player_animation_state, player_current_frame, \
        player_frame_counter, player_direction, game_state, \
        player_hp, player_xp

    damage = 5 + strength
    enemy["health"] -= damage
    log.append(f"You hit an {enemy['type']} for {damage} damage!")

    # Trigging goblin damage animation
    if enemy["type"] == "goblin":
        enemy["animation_state"] = "damaged"
        enemy["current_frame"] = 0
        enemy["frame_counter"] = 0

    player_animation_state = "attacking"
    player_current_frame = 0
    player_frame_counter = 0
    game_state = "player_animating"

    player_direction = "right" if dx > 0 else \
        "left" if dx < 0 else "down" if dy > 0 else "up"

    if enemy["health"] <= 0:
        enemy["animation_state"] = "dying"
        enemy["current_frame"] = 0
        enemy["frame_counter"] = 0
        xp_gain = (10 + current_level) if (
                enemy["type"] == "goblin") else (20 + current_level * 2)
        player_xp += xp_gain
        log.append(f"Gained {xp_gain} XP!")
        check_level_up()
    else:
        retaliation_damage = max(MIN_ENEMY_DAMAGE, enemy["damage"] - strength)
        player_hp -= retaliation_damage
        log.append(f"The {enemy['type']} "
                   f"retaliates for {retaliation_damage} damage!")
        if player_hp <= 0:
            log.append("You died!")
            game_over_screen()
            return


# Handling the chest interaction
def handle_interaction():
    global player_xp

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
        check_x = player_pos[0] + dx
        check_y = player_pos[1] + dy
        for treasure in treasures:
            if (treasure['x'] == check_x and treasure['y']
                    == check_y and treasure['state'] == 'closed'):
                treasure['state'] = 'open'
                potion_type = random.choices(list
                                             (POTION_WEIGHTS.keys()),
                                             weights=list(POTION_WEIGHTS.
                                                          values()), k=1)[0]
                inventory[f"{potion_type.capitalize()} Potion"] += 1
                player_xp += 5
                log.append(f"Found {potion_type.capitalize()} Potion!")
                check_level_up()


# Potion usage handler
def handle_potion_use(key):
    global player_hp, potion_selection, game_state

    potion_map = {pygame.K_1: "Small Potion",
                  pygame.K_2: "Medium Potion", pygame.K_3: "Large Potion"}
    potion = potion_map.get(key)
    if potion and inventory[potion] > 0:
        heal_amount = {"Small Potion": 10,
                       "Medium Potion": 20, "Large Potion": 30}[potion]
        player_hp = min(player_max_hp, player_hp + heal_amount)
        inventory[potion] -= 1
        log.append(f"Used {potion} (+{heal_amount} HP)!")
        potion_selection = False
        game_state = "enemy_turn"


# Player animation for attacking
def handle_player_animation():
    global player_frame_counter, player_current_frame, game_state

    player_frame_counter += 1
    if player_frame_counter >= 3:
        player_current_frame += 1
        player_frame_counter = 0
        if player_current_frame >= len(attack_right_sprites):
            player_animation_state = "idle"
            player_current_frame = 0
            game_state = "enemy_turn"


# Player animation for the getting damaged
def handle_player_damage_animation():
    global player_frame_counter, player_current_frame, player_animation_state

    player_frame_counter += 1
    if player_frame_counter >= 3:
        player_current_frame += 1
        player_frame_counter = 0
        if player_current_frame >= len(player_damage_frames):
            player_animation_state = "idle"
            player_current_frame = 0


# Enemy animations
def handle_enemy_animations():
    animations_done = True
    for enemy in enemies:
        if enemy["animation_state"] == "attacking":
            enemy["frame_counter"] += 1
            if enemy["frame_counter"] >= 5:
                enemy["current_frame"] += 1
                enemy["frame_counter"] = 0
                if (enemy["current_frame"] >= len
                    (goblin_attack_sprites if enemy["type"] ==
                        "goblin" else slime_attack_sprites)):
                    enemy["animation_state"] = "alive"
            if enemy["current_frame"] < len(goblin_attack_sprites
                                            if enemy["type"] == "goblin"
                                            else slime_attack_sprites):
                animations_done = False
    return animations_done


# Main menu screen initialization
def main_menu():
    # Load button images
    start_button = pygame.image.load("buttons/playbutton.png").convert_alpha()
    quit_button = pygame.image.load("buttons/quitbutton.png").convert_alpha()

    # Resize buttons
    button_width, button_height = 180, 50  # New button size
    start_button = pygame.transform.scale(start_button,
                                          (button_width, button_height))
    quit_button = pygame.transform.scale(quit_button,
                                         (button_width, button_height))

    # Load background image and scale it to fit the screen
    background = pygame.image.load("background.png").convert()
    background = pygame.transform.scale(background,
                                        (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Title font
    title_font = pygame.font.Font(FONT_PATH, 72)
    subtitle_font = pygame.font.Font(FONT_PATH, 56)

    # Title text
    title_text = title_font.render("Rogue-like Game", True, WHITE)
    subtitle_text = subtitle_font.render("Adventure Awaits!", True, WHITE)

    # Button positions (moved a bit lower)
    start_button_rect = start_button.get_rect(center=(SCREEN_WIDTH //
                                                      2, SCREEN_HEIGHT
                                                      // 2 + 50))
    quit_button_rect = quit_button.get_rect(center=(SCREEN_WIDTH //
                                                    2, SCREEN_HEIGHT
                                                    // 2 + 150))

    while True:
        # Draw background
        screen.blit(background, (0, 0))

        # Draw title with shadow
        shadow_offset = 5
        title_shadow = title_font.render("Rogue-like Game", True, BLACK)
        subtitle_shadow = subtitle_font.render("Adventure Awaits!",
                                               True, BLACK)
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 -
                                   title_text.get_width() // 2 +
                                   shadow_offset, 100 + shadow_offset))
        screen.blit(subtitle_shadow, (SCREEN_WIDTH // 2 -
                                      subtitle_text.get_width() // 2
                                      + shadow_offset, 180 + shadow_offset))
        screen.blit(title_text, (SCREEN_WIDTH // 2 -
                                 title_text.get_width() // 2, 100))
        screen.blit(subtitle_text, (SCREEN_WIDTH // 2 -
                                    subtitle_text.get_width() // 2, 180))

        # Draw buttons (without borders)
        screen.blit(start_button, start_button_rect)
        screen.blit(quit_button, quit_button_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    restart_game()
                    return
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(15)


# Options menu initialization
def options_menu():
    # Function for options menu
    menu_button = pygame.image.load("buttons/menu.png").convert_alpha()
    restart_button = pygame.image.load("buttons/"
                                       "restartbutton.png").convert_alpha()

    # Resize buttons
    button_width, button_height = 180, 50
    menu_button = pygame.transform.scale(menu_button,
                                         (button_width, button_height))
    restart_button = pygame.transform.scale(restart_button,
                                            (button_width, button_height))

    # Button positions
    menu_button_rect = menu_button.get_rect(center=(SCREEN_WIDTH // 2,
                                                    SCREEN_HEIGHT // 2 - 50))
    restart_button_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2,
                                                          SCREEN_HEIGHT // 2
                                                          + 50))

    while True:
        screen.fill(DARK_GRAY)
        title = options_font.render("Options", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Draw buttons
        screen.blit(menu_button, menu_button_rect)
        screen.blit(restart_button, restart_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if menu_button_rect.collidepoint(mouse_pos):
                    return "menu"
                elif restart_button_rect.collidepoint(mouse_pos):
                    restart_game()
                    return "restart"

        pygame.display.flip()
        clock.tick(15)


# Restarting the game from the begining
def restart_game():
    # Function for reseting the game to the original state
    global player_pos, player_hp, player_max_hp, inventory, \
        equipped_armor, inventory_open, \
        potion_selection, player_animation_state, \
        player_current_frame, player_frame_counter, \
        player_direction, player_xp, player_level, \
        xp_for_next_level, current_level, stat_points, \
        strength, vitality, log, visibility, treasures, \
        enemies, map_data, staircase_pos, themap
    # Reset player state
    player_pos = [GRID_WIDTH // 2, GRID_HEIGHT // 2]
    player_hp = 50
    player_max_hp = 50
    inventory = {
        "Small Potion": 0,
        "Medium Potion": 0,
        "Large Potion": 0
    }
    equipped_armor = {
        "helmet": None,
        "chestplate": None,
        "leggings": None,
        "boots": None
    }
    inventory_open = False
    potion_selection = False
    player_animation_state = "idle"
    player_current_frame = 0
    player_frame_counter = 0
    player_direction = "right"

    # Reset game state
    game_state = "player_turn"
    player_xp = 0
    player_level = 1
    xp_for_next_level = 10
    current_level = 1
    stat_points = 0
    strength = 1
    vitality = 1
    log = []

    # Reset visibility
    visibility = [[False for _ in range(GRID_WIDTH)]
                  for _ in range(GRID_HEIGHT)]

    # Reset dungeon map
    themap = Map()
    themap.makeMap(GRID_WIDTH, GRID_HEIGHT, fail=50, b1=50, mrooms=50)
    map_data = themap.mapArr
    staircase_pos = themap.staircase_pos

    # Reset player position to the first room
    first_room = themap.roomList[0]
    player_pos = [first_room[2] + first_room[0] //
                  2, first_room[3] + first_room[1] // 2]

    # Reset treasures and enemies
    treasures = generate_treasures(3)
    enemies = generate_enemies(5 + current_level)

    # Reveal the starting area
    reveal_area(player_pos[0], player_pos[1])


# Main function
def main():
    global font, game_state

    # Show the main menu
    main_menu()

    # Initialize the game state
    restart_game()

    # Start the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    option = options_menu()
                    if option == "menu":
                        main_menu()  # Return to the main menu
                    elif option == "restart":
                        restart_game()  # Restart the game
                    elif option == "back":
                        continue  # Continue playing (close the options menu)
                elif game_state == "player_turn":
                    handle_player_input(event)

        if game_state == "player_animating":
            handle_player_animation()
        elif game_state == "enemy_turn":
            move_enemies()
            if any(e["animation_state"] == "attacking" for e in enemies):
                game_state = "enemy_animating"
            else:
                game_state = "player_turn"
        elif game_state == "enemy_animating":
            if handle_enemy_animations():
                game_state = "player_turn"

        if player_animation_state == "damaged":
            handle_player_damage_animation()

        if (player_pos[0] == staircase_pos[0]
                and player_pos[1] == staircase_pos[1]):
            generate_new_level()

        screen.fill(BLACK)
        draw_map()
        draw_objects()
        draw_ui()
        if current_level == 3:
            draw_warg_health_bar()
        if inventory_open:
            draw_status_window()
        if potion_selection:
            draw_potion_selection()
        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    font = pygame.font.Font(FONT_PATH, 32)
    options_font = pygame.font.Font(FONT_PATH, 48)

    main()
