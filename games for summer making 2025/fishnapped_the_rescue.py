import pygame
import sys
import random
import math

pygame.init()

# === Load images ===
menu = pygame.image.load("menu.png")
sw_village = pygame.image.load("sw_vil.png")
sw_farm = pygame.image.load("sw_far.png")
sw_mar = pygame.image.load("sw_mar.png")
forest1 = pygame.image.load("forest_1.png")
forest2 = pygame.image.load("forest_2.png")
forest3 = pygame.image.load("forest_3.png")
road_mud = pygame.image.load("road_mud.png")
dog_white = pygame.image.load("dog.png")
boss_p = pygame.image.load("boss.png")
boss_killed = pygame.image.load("boss_killed.png")
killed_Ending = pygame.image.load("killed_ending.png")

scroll_width = 200
scroll_height = 720
full_height = scroll_height * 6

scroll_bg = pygame.Surface((scroll_width, full_height), pygame.SRCALPHA)
scroll_bg.blit(sw_village, (0, 0))
scroll_bg.blit(sw_mar, (0, scroll_height))
scroll_bg.blit(sw_farm, (0, scroll_height * 2))
scroll_bg.blit(forest1, (0, scroll_height * 3))
scroll_bg.blit(forest2, (0, scroll_height * 4))
scroll_bg.blit(forest3, (0, scroll_height * 5))

scroll_y = 0
scroll_speed = 3
road_scroll_y = 0
road_scroll_speed = 0.1

# === Display setup ===
WIDTH, HEIGHT = 1280, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fishnapped - Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
RED = (255, 0, 0)

title_font = pygame.font.SysFont("comicsans", 60)
button_font = pygame.font.SysFont("comicsans", 40)

road_width, road_height = road_mud.get_size()
full_road_height = road_height * 2

scrolling_road = pygame.Surface((road_width, full_road_height)).convert()
scrolling_road.blit(road_mud, (0, 0))
scrolling_road.blit(road_mud, (0, road_height))

cat_run_frames = [
    pygame.image.load("cat_r1.png").convert_alpha(),
    pygame.image.load("cat_r2.png").convert_alpha(),
    pygame.image.load("cat_r3.png").convert_alpha(),
    pygame.image.load("cat_r4.png").convert_alpha(),
    pygame.image.load("cat_r5.png").convert_alpha()
]

bullet_C = pygame.image.load("attack_c.png").convert_alpha()

def draw_menu():
    win.blit(menu, (0, 0))
    pygame.display.update()

def menu_loop():
    in_menu = True
    while in_menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    in_menu = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def draw_next_level():
    win.fill(BLACK)
    msg = title_font.render("All enemies defeated! Proceed to next level?", True, YELLOW)
    cont = button_font.render("Press ENTER to Continue", True, WHITE)
    win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 250))
    win.blit(cont, (WIDTH // 2 - cont.get_width() // 2, HEIGHT // 2 - 150))
    pygame.display.update()

def show_next_level_menu():
    waiting = True
    while waiting:
        draw_next_level()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def show_ending(screen, image):
    screen.blit(image, (0, 0))
    pygame.display.update()
    pygame.time.delay(5000)

def shoot_boss_bullets(center_x, center_y, boss_bullets_list):
    angles = [0, -20, -40, 20, 40]
    speed = 5
    for angle in angles:
        rad = math.radians(angle)
        vx = speed * math.sin(rad)
        vy = speed * math.cos(rad)
        boss_bullets_list.append([center_x, center_y, vx, vy])

def start_game():
    global scroll_y
    road_scroll_y = 0

    level = 1
    is_boss_level = False
    boss = None
    boss_health = 0

    cat_x = 100
    cat_y = 500
    cat_width = 50
    cat_height = 50
    cat_speed = 5
    LEFT_LIMIT = 200
    RIGHT_LIMIT = WIDTH - 200 - cat_width

    bullets = []
    enemy_bullets = []
    bullet_speed = 5
    enemy_bullet_speed = 5
    last_shot = 0
    last_enemy_shot = 0
    enemy_shoot_delay = 1000

    enemy_rows = 3
    enemy_cols = 6
    enemy_width = 50
    enemy_height = 50
    enemy_speed = 3
    enemy_direction = 1
    wall_hits = 0

    enemies = []
    for row in range(enemy_rows):
        for col in range(enemy_cols):
            enemy_x = 200 + col * 100
            enemy_y = 100 + row * 60
            enemies.append([enemy_x, enemy_y])

    current_frame = 0
    frame_timer = 0
    frame_speed = 10

    clock = pygame.time.Clock()
    running = True
    boss_bullets = []
    boss_bullets = []
    boss_shoot_delay = 5000
    boss_last_shot = 0
    burst_count = 0
    burst_limit = 2
    burst_interval = 300
    last_burst_time = 0
    while running:
        clock.tick(60)

        # Background scroll
        scroll_y = (scroll_y - scroll_speed) % full_height
        road_scroll_y = (road_scroll_y - scroll_speed) % road_height

        win.blit(scroll_bg, (0, -scroll_y))
        win.blit(scroll_bg, (0, full_height - scroll_y))
        win.blit(scroll_bg, (WIDTH - scroll_width, -scroll_y))
        win.blit(scroll_bg, (WIDTH - scroll_width, full_height - scroll_y))
        win.blit(scrolling_road, (200, -road_scroll_y))
        win.blit(scrolling_road, (200, road_height - road_scroll_y))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys[pygame.K_RIGHT] and cat_x < RIGHT_LIMIT:
            cat_x += cat_speed
        if keys[pygame.K_LEFT] and cat_x > LEFT_LIMIT:
            cat_x -= cat_speed

        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_shot > 500:
            bullet_x = cat_x + cat_width // 2 - 5
            bullet_y = cat_y
            bullets.append([bullet_x, bullet_y])
            last_shot = current_time

        if current_time - last_enemy_shot > enemy_shoot_delay and enemies:
            shooter = random.choice(enemies)
            bullet_x = shooter[0] + enemy_width // 2 - 5
            bullet_y = shooter[1] + enemy_height
            enemy_bullets.append([bullet_x, bullet_y])
            last_enemy_shot = current_time

        # Bullet logic
        for bullet in bullets:
            bullet[1] -= bullet_speed
            win.blit(bullet_C, (bullet[0], bullet[1]))
        bullets = [b for b in bullets if b[1] > 0]

        for bullet in enemy_bullets:
            bullet[1] += enemy_bullet_speed
            pygame.draw.rect(win, RED, (bullet[0], bullet[1], 10, 20))
        enemy_bullets = [b for b in enemy_bullets if b[1] < HEIGHT]

        # Enemy movement
        move_down = False
        for enemy in enemies:
            enemy[0] += enemy_speed * enemy_direction
            if enemy[0] <= LEFT_LIMIT or enemy[0] + enemy_width >= RIGHT_LIMIT:
                move_down = True

        if move_down:
            wall_hits += 1
            enemy_direction *= -1
            if wall_hits >= 5:
                for enemy in enemies:
                    enemy[1] += 30
                wall_hits = 0

        # Bullet collisions with enemies
        new_enemies = []
        for enemy in enemies:
            hit = False
            for bullet in bullets:
                if (enemy[0] < bullet[0] < enemy[0] + enemy_width and
                    enemy[1] < bullet[1] < enemy[1] + enemy_height):
                    hit = True
                    bullets.remove(bullet)
                    break
            if not hit:
                new_enemies.append(enemy)
        enemies = new_enemies

        # Check if level completed
        if not enemies and not is_boss_level:
            level += 1
            show_next_level_menu()
            if level == 3:
                is_boss_level = True
                boss = [WIDTH // 2 - 50, 100, 100, 100]
                boss_health = 200
            else:
                enemies = []
                
                for row in range(enemy_rows):
                    for col in range(enemy_cols):
                        enemy_x = 200 + col * 100
                        enemy_y = 100 + row * 60
                        enemies.append([enemy_x, enemy_y])
                wall_hits = 0

        # Check player hit by bullet
        for bullet in enemy_bullets:
            if (cat_x < bullet[0] < cat_x + cat_width and
                cat_y < bullet[1] < cat_y + cat_height):
                show_ending(win, killed_Ending)
                running = False
        for bullet in boss_bullets:
            bullet[0] += bullet[2]  
            pygame.draw.circle(win, RED, (int(bullet[0]), int(bullet[1])), 8)

            if (cat_x < bullet[0] < cat_x + cat_width and
                cat_y < bullet[1] < cat_y + cat_height):
                show_ending(win, killed_Ending)
                running = False

        # Draw enemies
        for enemy in enemies:
            win.blit(dog_white, (enemy[0], enemy[1]))
 
        # Boss fight
        if is_boss_level and boss:
            win.blit(boss_p, (boss[0], boss[1]))
            if current_time - boss_last_shot > boss_shoot_delay and burst_count == 0:
                burst_count = burst_limit
                last_burst_time = current_time
                boss_last_shot = current_time

            if burst_count > 0 and current_time - last_burst_time >= burst_interval:
                shoot_boss_bullets(boss[0] + boss[2] // 2, boss[1] + boss[3], boss_bullets)
                last_burst_time = current_time
                burst_count -= 1
            for b in boss_bullets:
                b[0] += b[2]  # vx
                b[1] += b[3]  # vy
                pygame.draw.circle(win, (255, 50, 50), (int(b[0]), int(b[1])), 8)

            boss_bullets = [b for b in boss_bullets if 0 <= b[0] <= WIDTH and 0 <= b[1] <= HEIGHT]



            hit_bullets = []
            for bullet in bullets:
                if (boss[0] < bullet[0] < boss[0] + boss[2] and
                    boss[1] < bullet[1] < boss[1] + boss[3]):
                    boss_health -= 1000
                    hit_bullets.append(bullet)
            for b in hit_bullets:
                bullets.remove(b)

            if boss_health <= 0:
                show_ending(win, boss_killed)
                running = False
        
        # Animate cat
        frame_timer += 1
        if frame_timer >= frame_speed:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(cat_run_frames)

        win.blit(cat_run_frames[current_frame], (cat_x, cat_y))

        pygame.display.update()

    pygame.quit()
    sys.exit()

menu_loop()
start_game()
