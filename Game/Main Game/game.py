import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer with Coins, Enemies, and Power-Ups")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)


player_width = 10
player_height = 50
player_color = RED
player_x = WIDTH // 2
player_y = HEIGHT - player_height - 20 
player_velocity = 5
jump_strength = 10
gravity = 0.5
player_y_velocity = 0
is_jumping = False

coin_radius = 10
score = 0


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 50
        self.color = RED

    def draw(self, screen):
       
        pygame.draw.circle(screen, self.color, (self.x + self.width // 2, self.y - self.height // 2), 10)
       
        pygame.draw.line(screen, self.color, (self.x + self.width // 2, self.y - self.height // 2 + 10), (self.x + self.width // 2, self.y), 2)
       
        pygame.draw.line(screen, self.color, (self.x + self.width // 2, self.y - self.height // 4), (self.x, self.y - self.height // 4 + 10), 2)
        pygame.draw.line(screen, self.color, (self.x + self.width // 2, self.y - self.height // 4), (self.x + self.width, self.y - self.height // 4 + 10), 2)
    
        pygame.draw.line(screen, self.color, (self.x + self.width // 2, self.y), (self.x, self.y + self.height // 4), 2)
        pygame.draw.line(screen, self.color, (self.x + self.width // 2, self.y), (self.x + self.width, self.y + self.height // 4), 2)
       
        pygame.draw.line(screen, self.color, (self.x + self.width, self.y - self.height // 4 + 10), (self.x + self.width + 10, self.y - self.height // 4 + 5), 2)


power_ups = [
    pygame.Rect(100, HEIGHT - 40, 20, 20)    # Auf dem Boden
]
power_up_active = False
power_up_timer = 0


font = pygame.font.SysFont(None, 36)


clock = pygame.time.Clock()
running = True
shop_open = False

# you can remove some levels if you want
levels = [
    {
        'platforms': [
            pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
            pygame.Rect(150, HEIGHT - 100, 100, 20),
            pygame.Rect(300, HEIGHT - 200, 100, 20),
            pygame.Rect(450, HEIGHT - 150, 100, 20),
            pygame.Rect(600, HEIGHT - 250, 100, 20)
        ],
        'coins': [
            (175, HEIGHT - 120),
            (325, HEIGHT - 220),
            (475, HEIGHT - 170),
            (625, HEIGHT - 270)
        ],
        'enemies': [
            Enemy(200, HEIGHT - 120),
            Enemy(350, HEIGHT - 220),
            Enemy(500, HEIGHT - 170),
            Enemy(650, HEIGHT - 270)
        ]
    },
    {
        'platforms': [
            pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
            pygame.Rect(200, HEIGHT - 150, 150, 20),
            pygame.Rect(400, HEIGHT - 250, 150, 20),
            pygame.Rect(650, HEIGHT - 300, 100, 20),
            pygame.Rect(100, HEIGHT - 350, 100, 20)
        ],
        'coins': [
            (225, HEIGHT - 170),
            (425, HEIGHT - 270),
            (675, HEIGHT - 320),
            (125, HEIGHT - 370)
        ],
        'enemies': [
            Enemy(250, HEIGHT - 170),
            Enemy(450, HEIGHT - 270),
            Enemy(700, HEIGHT - 320),
            Enemy(150, HEIGHT - 370)
        ]
    },
    {
        'platforms': [
            pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
            pygame.Rect(150, HEIGHT - 100, 100, 20),
            pygame.Rect(300, HEIGHT - 200, 100, 20),
            pygame.Rect(450, HEIGHT - 150, 100, 20),
            pygame.Rect(600, HEIGHT - 250, 100, 20),
            pygame.Rect(750, HEIGHT - 300, 50, 20),
            pygame.Rect(50, HEIGHT - 350, 50, 20)
        ],
        'coins': [
            (175, HEIGHT - 120),
            (325, HEIGHT - 220),
            (475, HEIGHT - 170),
            (625, HEIGHT - 270),
            (775, HEIGHT - 320),
            (75, HEIGHT - 370)
        ],
        'enemies': [
            Enemy(200, HEIGHT - 120),
            Enemy(350, HEIGHT - 220),
            Enemy(500, HEIGHT - 170),
            Enemy(650, HEIGHT - 270),
            Enemy(800, HEIGHT - 320),
            Enemy(100, HEIGHT - 370)
        ]
    }
]

current_level = 0
time_limit = 60 * 60  # 1 Minute in Frames
timer = time_limit

# Skins
skins = [RED, BLUE, GREEN, YELLOW, GOLD]
skin_prices = [5, 10, 15]  # Preise für Skins
current_skin_index = 0

def draw_stick_figure(screen, x, y, color):
    # Kopf
    pygame.draw.circle(screen, color, (x + player_width // 2, y - player_height // 2), 10)
    # Körper
    pygame.draw.line(screen, color, (x + player_width // 2, y - player_height // 2 + 10), (x + player_width // 2, y), 2)
    # Arme
    pygame.draw.line(screen, color, (x + player_width // 2, y - player_height // 4), (x, y - player_height // 4 + 10), 2)
    pygame.draw.line(screen, color, (x + player_width // 2, y - player_height // 4), (x + player_width, y - player_height // 4 + 10), 2)
    # Beine
    pygame.draw.line(screen, color, (x + player_width // 2, y), (x, y + player_height // 4), 2)
    pygame.draw.line(screen, color, (x + player_width // 2, y), (x + player_width, y + player_height // 4), 2)

def draw_blue_rabbit(screen, x, y):
    pygame.draw.circle(screen, BLUE, (x + player_width // 2, y - player_height // 2), 10)  # Kopf
    pygame.draw.line(screen, BLUE, (x + player_width // 2, y - player_height // 2 + 10), (x + player_width // 2, y), 2)  # Körper
    pygame.draw.line(screen, BLUE, (x + player_width // 2, y - player_height // 4), (x, y - player_height // 4 + 10), 2)  # Arme
    pygame.draw.line(screen, BLUE, (x + player_width // 2, y - player_height // 4), (x + player_width, y - player_height // 4 + 10), 2)  # Arme
    pygame.draw.line(screen, BLUE, (x + player_width // 2, y), (x, y + player_height // 4), 2)  # Beine
    pygame.draw.line(screen, BLUE, (x + player_width // 2, y), (x + player_width, y + player_height // 4), 2)  # Beine

def draw_yellow_car(screen, x, y):
    pygame.draw.rect(screen, YELLOW, (x, y - player_height // 2, player_width, player_height // 2))  # Auto-Körper
    pygame.draw.circle(screen, BLACK, (x + player_width // 4, y), player_width // 4)  # Räder
    pygame.draw.circle(screen, BLACK, (x + 3 * player_width // 4, y), player_width // 4)  # Räder

def draw_gold_nike_logo(screen, x, y):
    pygame.draw.polygon(screen, GOLD, [(x, y), (x + player_width, y - player_height // 2), (x + player_width, y)])  # Nike-Logo

def draw_shop(screen, skins, skin_prices, score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 36)
    shop_text = font.render("Shop", True, WHITE)
    screen.blit(shop_text, (WIDTH // 2 - shop_text.get_width() // 2, 50))
    for i, (skin, price) in enumerate(zip(skins[1:], skin_prices)):
        skin_rect = pygame.Rect(WIDTH // 2 - 50, 100 + i * 100, 100, 50)
        pygame.draw.rect(screen, skin, skin_rect)
        price_text = font.render(f"{price} Coins", True, WHITE)
        screen.blit(price_text, (WIDTH // 2 - price_text.get_width() // 2, 160 + i * 100))
        # Zeichne den Skin als Hintergrund
        if skin == BLUE:
            draw_blue_rabbit(screen, WIDTH // 2, 100 + i * 100 + 25)
        elif skin == YELLOW:
            draw_yellow_car(screen, WIDTH // 2, 100 + i * 100 + 25)
        elif skin == GOLD:
            draw_gold_nike_logo(screen, WIDTH // 2, 100 + i * 100 + 25)
    
    score_surf = font.render(f"Coins: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))
    
    pygame.display.flip()

def draw_button(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont(None, 36)
    text_surf = font.render(text, True, WHITE)
    screen.blit(text_surf, (x + (width - text_surf.get_width()) // 2, y + (height - text_surf.get_height()) // 2))

# Shop-Button
shop_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 50, 140, 40)

# Schießen-Logik
bullets = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shop_button_rect.collidepoint(event.pos):
                shop_open = not shop_open
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not shop_open:
                is_jumping = True
                player_y_velocity = -jump_strength
            if event.key == pygame.K_f and not shop_open:
                # Schießen
                bullets.append(pygame.Rect(player_x + player_width, player_y + player_height // 2, 10, 5))
            if event.key == pygame.K_ESCAPE and shop_open:
                shop_open = False

    if shop_open:
        # Shop-UI anzeigen und Kauf-Logik
        draw_shop(screen, skins, skin_prices, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, price in enumerate(skin_prices):
                    if pygame.Rect(WIDTH // 2 - 50, 100 + i * 100, 100, 50).collidepoint(event.pos):
                        if score >= price:
                            score -= price
                            current_skin_index = i + 1
                            player_color = skins[current_skin_index]
                            shop_open = False
    else:
        # Tastatureingaben
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Nach links mit 'A'
            player_x -= player_velocity
        if keys[pygame.K_d]:  # Nach rechts mit 'D'
            player_x += player_velocity

        # Schwerkraft anwenden
        if is_jumping:
            player_y_velocity += gravity
            player_y += player_y_velocity

            # Kollision mit Plattformen
            for platform in levels[current_level]['platforms']:
                if player_y + player_height >= platform.top and player_y + player_height - player_y_velocity < platform.top and platform.left < player_x < platform.right:
                    player_y = platform.top - player_height
                    is_jumping = False
                    player_y_velocity = 0

        # Kollision mit Münzen prüfen
        collected_coins = [coin for coin in levels[current_level]['coins'] if pygame.Rect(coin[0] - coin_radius, coin[1] - coin_radius, coin_radius * 2, coin_radius * 2).colliderect(pygame.Rect(player_x, player_y, player_width, player_height))]
        for coin in collected_coins:
            levels[current_level]['coins'].remove(coin)
            score += 1

        # Kollision mit Feinden prüfen
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if any(player_rect.colliderect(pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)) for enemy in levels[current_level]['enemies']):
            current_level = 0
            player_x = WIDTH // 2
            player_y = HEIGHT - player_height - 20
            timer = time_limit
            score = 0

        # Schießen
        for bullet in bullets:
            bullet.x += 10
            if bullet.x > WIDTH:
                bullets.remove(bullet)
            for enemy in levels[current_level]['enemies']:
                if bullet.colliderect(pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                    levels[current_level]['enemies'].remove(enemy)
                    bullets.remove(bullet)

        # Kollision mit Power-Ups prüfen
        collected_power_ups = [power_up for power_up in power_ups if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(power_up)]
        if collected_power_ups:
            power_up_active = True
            power_up_timer = 300  # Power-Up für 300 Frames aktiv
            for power_up in collected_power_ups:
                power_ups.remove(power_up)

        # Power-Up aktivieren
        if power_up_active:
            player_velocity = 10  # Spieler schneller machen
            power_up_timer -= 1
            if power_up_timer <= 0:
                power_up_active = False
                player_velocity = 5

        # Bildschirm füllen
        screen.fill(BLACK)

        # Plattformen zeichnen
        for platform in levels[current_level]['platforms']:
            pygame.draw.rect(screen, WHITE, platform)

        # Spieler zeichnen
        if current_skin_index == 0:
            draw_stick_figure(screen, player_x, player_y + player_height, player_color)
        elif current_skin_index == 1:
            draw_blue_rabbit(screen, player_x, player_y + player_height)
        elif current_skin_index == 2:
            draw_yellow_car(screen, player_x, player_y + player_height)
        elif current_skin_index == 3:
            draw_gold_nike_logo(screen, player_x, player_y + player_height)

        # Münzen zeichnen
        for coin in levels[current_level]['coins']:
            pygame.draw.circle(screen, YELLOW, coin, coin_radius)

        # Feinde zeichnen
        for enemy in levels[current_level]['enemies']:
            enemy.draw(screen)

        # Power-Ups zeichnen
        for power_up in power_ups:
            pygame.draw.rect(screen, GREEN, power_up)

        # Schüsse zeichnen
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Punktestand anzeigen
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Timer anzeigen
        timer -= 1
        if timer <= 0:
            current_level = 0
            player_x = WIDTH // 2
            player_y = HEIGHT - player_height - 20
            timer = time_limit
            score = 0
        timer_text = font.render(f"Time: {timer // 60}", True, WHITE)
        screen.blit(timer_text, (WIDTH - 150, 10))

        # Level abschließen, wenn alle Münzen eingesammelt sind
        if not levels[current_level]['coins']:
            current_level += 1
            if current_level >= len(levels):
                current_level = 0
                score = 0  # Punkte zurücksetzen
            player_x = WIDTH // 2
            player_y = HEIGHT - player_height - 20
            timer = time_limit

        # Shop-Button zeichnen
        draw_button(screen, "Shop", shop_button_rect.x, shop_button_rect.y, shop_button_rect.width, shop_button_rect.height, BLUE)

        # Bildschirm aktualisieren
        pygame.display.flip()

        # Framerate
        clock.tick(60)