import random
import sys
from pathlib import Path

import pygame

# Roguelike Snake — Neon Dungeon
WIDTH, HEIGHT = 900, 650
CELL = 25
COLS, ROWS = WIDTH // CELL, (HEIGHT - 50) // CELL
FPS = 60
SAVE_FILE = Path.home() / ".roguelike_snake_best"

BG = (10, 14, 28)
PANEL = (20, 29, 51)
GRID = (25, 37, 60)
CYAN = (56, 230, 220)
GREEN = (96, 240, 150)
GOLD = (255, 205, 85)
RED = (255, 90, 115)
WHITE = (235, 242, 255)
MUTED = (145, 163, 190)
PURPLE = (174, 117, 255)


def load_best():
    try:
        return int(SAVE_FILE.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return 0


def save_best(value):
    try:
        SAVE_FILE.write_text(str(value), encoding="utf-8")
    except OSError:
        pass


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Roguelike Snake — Neon Dungeon")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.small = pygame.font.SysFont("consolas", 15)
        self.big = pygame.font.SysFont("consolas", 42, bold=True)
        self.best = load_best()
        self.state = "menu"
        self.reset()

    def reset(self):
        center = (COLS // 2, ROWS // 2)
        self.snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.crystals = 0
        self.floor = 1
        self.score = 0
        self.hp = 3
        self.shield = 0
        self.bonus = 0
        self.speed_level = 0
        self.obstacles = set()
        self.food = None
        self.upgrade_choices = []
        self.upgrades_pending = 0
        self.paused_from = "playing"
        self.spawn_food()
        self.spawn_obstacles(5)

    def occupied(self):
        return set(self.snake) | self.obstacles

    def random_empty(self):
        available = [(x, y) for x in range(COLS) for y in range(ROWS)
                     if (x, y) not in self.occupied()]
        return random.choice(available) if available else None

    def spawn_food(self):
        self.food = self.random_empty()

    def spawn_obstacles(self, count):
        for _ in range(count):
            point = self.random_empty()
            if point is not None:
                self.obstacles.add(point)

    def start(self):
        if self.state == "menu" or self.state == "gameover":
            self.reset()
        self.state = "playing"

    def move(self):
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        dx, dy = self.direction
        head = (hx + dx, hy + dy)
        growing = head == self.food
        body = self.snake if growing else self.snake[:-1]

        if (head[0] < 0 or head[0] >= COLS or head[1] < 0 or head[1] >= ROWS
                or head in body or head in self.obstacles):
            if self.shield > 0:
                self.shield -= 1
                self.obstacles.discard(head)
                head = self.random_empty()
                if head is None:
                    self.state = "gameover"
                    return
                self.snake.insert(0, head)
                self.snake.pop()
                return
            self.hp -= 1
            if self.hp <= 0:
                self.state = "gameover"
                self.best = max(self.best, self.score)
                save_best(self.best)
                return
            # Respawn the snake but keep the run's upgrades and score.
            center = (COLS // 2, ROWS // 2)
            self.snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
            self.direction = self.next_direction = (1, 0)
            return

        self.snake.insert(0, head)
        if growing:
            self.crystals += 1
            self.score += 10 + self.bonus
            self.best = max(self.best, self.score)
            save_best(self.best)
            if self.crystals % 3 == 0:
                self.upgrades_pending = 1
                self.state = "upgrade"
                self.upgrade_choices = random.sample(
                    [("speed", "Tăng tốc", "Rắn di chuyển nhanh hơn"),
                     ("vitality", "Sinh lực", "Hồi 1 mạng (tối đa 5)"),
                     ("bonus", "Tinh thể quý", "+5 điểm mỗi tinh thể"),
                     ("shield", "Khiên năng lượng", "Chặn một lần va chạm")], 3)
            if self.crystals % 5 == 0:
                self.floor += 1
                self.spawn_obstacles(min(3 + self.floor, 12))
            self.spawn_food()
        else:
            self.snake.pop()
        if self.food is None:
            self.state = "gameover"

    def apply_upgrade(self, index):
        if not 0 <= index < len(self.upgrade_choices):
            return
        kind = self.upgrade_choices[index][0]
        if kind == "speed":
            self.speed_level = min(8, self.speed_level + 1)
        elif kind == "vitality":
            self.hp = min(5, self.hp + 1)
        elif kind == "bonus":
            self.bonus += 5
        elif kind == "shield":
            self.shield += 1
        self.state = "playing"

    def draw_text(self, text, x, y, color=WHITE, font=None, center=False):
        image = (font or self.font).render(text, True, color)
        rect = image.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(image, rect)

    def draw(self):
        self.screen.fill(BG)
        pygame.draw.rect(self.screen, PANEL, (0, 0, WIDTH, 50))
        self.draw_text("NEON DUNGEON", 18, 15, CYAN)
        self.draw_text(f"ĐIỂM {self.score}", 260, 15, GOLD)
        self.draw_text(f"♥ {self.hp}", 430, 15, RED)
        self.draw_text(f"TẦNG {self.floor}", 530, 15, PURPLE)
        self.draw_text(f"KỶ LỤC {self.best}", 680, 15, MUTED)

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, GRID, (x, 50), (x, HEIGHT))
        for y in range(50, HEIGHT, CELL):
            pygame.draw.line(self.screen, GRID, (0, y), (WIDTH, y))

        for x, y in self.obstacles:
            rect = pygame.Rect(x * CELL + 3, 50 + y * CELL + 3, CELL - 6, CELL - 6)
            pygame.draw.rect(self.screen, (105, 50, 83), rect, border_radius=5)
            pygame.draw.rect(self.screen, RED, rect, 1, border_radius=5)

        if self.food is not None:
            x, y = self.food
            pygame.draw.circle(self.screen, GOLD,
                               (x * CELL + CELL // 2, 50 + y * CELL + CELL // 2), 8)
            pygame.draw.circle(self.screen, WHITE,
                               (x * CELL + CELL // 2 - 2, 50 + y * CELL + CELL // 2 - 2), 2)

        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * CELL + 2, 50 + y * CELL + 2, CELL - 4, CELL - 4)
            color = CYAN if i == 0 else GREEN
            pygame.draw.rect(self.screen, color, rect, border_radius=7)
            if i == 0:
                cx, cy = rect.center
                pygame.draw.circle(self.screen, BG, (cx - 4, cy - 3), 2)
                pygame.draw.circle(self.screen, BG, (cx + 4, cy - 3), 2)

        footer = f"Tinh thể: {self.crystals}   Khiên: {self.shield}   Nâng cấp: {self.speed_level + self.bonus // 5}"
        self.draw_text(footer, 18, HEIGHT - 25, MUTED, self.small)

        if self.state != "playing":
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((5, 9, 22, 210))
            self.screen.blit(shade, (0, 0))
            if self.state == "menu":
                self.draw_text("ROGUELIKE SNAKE", WIDTH // 2, 210, CYAN, self.big, True)
                self.draw_text("NEON DUNGEON", WIDTH // 2, 260, PURPLE, self.font, True)
                self.draw_text("WASD / phím mũi tên: di chuyển", WIDTH // 2, 330, WHITE, self.font, True)
                self.draw_text("P: tạm dừng     ESC: thoát", WIDTH // 2, 365, MUTED, self.font, True)
                self.draw_text("Nhấn ENTER để bắt đầu", WIDTH // 2, 430, GOLD, self.font, True)
            elif self.state == "paused":
                self.draw_text("TẠM DỪNG", WIDTH // 2, 280, GOLD, self.big, True)
                self.draw_text("Nhấn P hoặc ENTER để tiếp tục", WIDTH // 2, 350, WHITE, self.font, True)
            elif self.state == "upgrade":
                self.draw_text("CHỌN NÂNG CẤP", WIDTH // 2, 175, CYAN, self.big, True)
                for i, choice in enumerate(self.upgrade_choices):
                    y = 245 + i * 88
                    rect = pygame.Rect(WIDTH // 2 - 250, y - 25, 500, 68)
                    pygame.draw.rect(self.screen, PANEL, rect, border_radius=10)
                    pygame.draw.rect(self.screen, PURPLE, rect, 1, border_radius=10)
                    self.draw_text(f"{i + 1}. {choice[1]}", WIDTH // 2, y - 5, GOLD, self.font, True)
                    self.draw_text(choice[2], WIDTH // 2, y + 22, MUTED, self.small, True)
            elif self.state == "gameover":
                self.draw_text("KẾT THÚC LƯỢT CHƠI", WIDTH // 2, 250, RED, self.big, True)
                self.draw_text(f"Điểm của bạn: {self.score}", WIDTH // 2, 325, WHITE, self.font, True)
                self.draw_text("Nhấn ENTER để chơi lại", WIDTH // 2, 390, GOLD, self.font, True)

        pygame.display.flip()

    def run(self):
        move_timer = 0
        running = True
        while running:
            dt = self.clock.tick(FPS)
            move_timer += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.state in ("menu", "gameover"):
                            self.start()
                        elif self.state == "paused":
                            self.state = "playing"
                    elif event.key == pygame.K_p:
                        if self.state == "playing":
                            self.state = "paused"
                        elif self.state == "paused":
                            self.state = "playing"
                    elif self.state == "upgrade" and event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        self.apply_upgrade(event.key - pygame.K_1)
                    elif self.state == "playing":
                        mapping = {
                            pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
                            pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
                            pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
                            pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
                        }
                        new_direction = mapping.get(event.key)
                        if new_direction and new_direction != (-self.direction[0], -self.direction[1]):
                            self.next_direction = new_direction

            if self.state == "playing":
                interval = max(65, 145 - self.speed_level * 10 - (self.floor - 1) * 3)
                if move_timer >= interval:
                    move_timer = 0
                    self.move()
            else:
                move_timer = 0
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    SnakeGame().run()
