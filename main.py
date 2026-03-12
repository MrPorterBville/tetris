import sys

import pygame

import prefabs as pre
from shape import Piece, PieceQueue

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60

GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 32
GRID_X = 180
GRID_Y = 70

FALL_EVENT = pygame.USEREVENT + 1
FALL_MS = 500


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.flashy_font = pygame.font.SysFont("impact", 34)
        self.flashy_label_font = pygame.font.SysFont("impact", 22)

        self.running = True
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False

        self.board = [["x" for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        self.piece_queue = PieceQueue(GRID_WIDTH, preview_count=3)
        self.current_piece = self.piece_queue.pull()
        self.saved_piece = None
        self.hold_used = False
        self.pause_button_rect = pygame.Rect(0, 0, 0, 0)

        pygame.time.set_timer(FALL_EVENT, FALL_MS)

    def collides(self, piece, x_off=0, y_off=0, new_shape=None):
        shape = new_shape if new_shape is not None else piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if not cell:
                    continue

                nx = piece.x + x + x_off
                ny = piece.y + y + y_off

                if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                    return True
                if ny >= 0 and self.board[nx][ny] != "x":
                    return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    bx = self.current_piece.x + x
                    by = self.current_piece.y + y
                    if 0 <= bx < GRID_WIDTH and 0 <= by < GRID_HEIGHT:
                        self.board[bx][by] = self.current_piece.kind

        cleared = self.clear_lines()
        if cleared > 0:
            self.lines += cleared
            self.score += [0, 100, 300, 500, 800][cleared] * self.level
            self.level = 1 + self.lines // 10
            speed = max(100, FALL_MS - (self.level - 1) * 35)
            pygame.time.set_timer(FALL_EVENT, speed)

        self.current_piece = self.piece_queue.pull()
        self.hold_used = False
        if self.collides(self.current_piece):
            self.game_over = True

    def hold_piece(self):
        if self.hold_used:
            return

        if self.saved_piece is None:
            self.saved_piece = Piece(self.current_piece.kind, GRID_WIDTH)
            self.current_piece = self.piece_queue.pull()
        else:
            swap_kind = self.saved_piece.kind
            self.saved_piece = Piece(self.current_piece.kind, GRID_WIDTH)
            self.current_piece = Piece(swap_kind, GRID_WIDTH)

        self.hold_used = True
        if self.collides(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        remaining_rows = []
        cleared = 0

        for y in range(GRID_HEIGHT):
            full = True
            for x in range(GRID_WIDTH):
                if self.board[x][y] == "x":
                    full = False
                    break
            if full:
                cleared += 1
            else:
                remaining_rows.append([self.board[x][y] for x in range(GRID_WIDTH)])

        for _ in range(cleared):
            remaining_rows.insert(0, ["x" for _ in range(GRID_WIDTH)])

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.board[x][y] = remaining_rows[y][x]

        return cleared

    def move(self, dx, dy):
        if not self.collides(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate(self):
        rotated = self.current_piece.rotated()
        for kick in [0, -1, 1, -2, 2]:
            if not self.collides(self.current_piece, kick, 0, rotated):
                self.current_piece.x += kick
                self.current_piece.shape = rotated
                return

    def hard_drop(self):
        while self.move(0, 1):
            pass
        self.lock_piece()

    def restart(self):
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.board = [["x" for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        self.piece_queue = PieceQueue(GRID_WIDTH, preview_count=3)
        self.current_piece = self.piece_queue.pull()
        self.saved_piece = None
        self.hold_used = False
        pygame.time.set_timer(FALL_EVENT, FALL_MS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.pause_button_rect.collidepoint(event.pos) and not self.game_over:
                    self.paused = not self.paused

            if event.type == FALL_EVENT and not self.game_over and not self.paused:
                if not self.move(0, 1):
                    self.lock_piece()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart()
                if event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused
                if self.paused:
                    continue
                if self.game_over:
                    continue

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.move(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.move(1, 0)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if not self.move(0, 1):
                        self.lock_piece()
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.rotate()
                elif event.key == pygame.K_SPACE:
                    self.hard_drop()
                elif event.key in (pygame.K_c, pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.hold_piece()

    def draw_board(self):
        board_px_w = GRID_WIDTH * BLOCK_SIZE
        board_px_h = GRID_HEIGHT * BLOCK_SIZE
        pygame.draw.rect(
            self.screen,
            (90, 90, 90),
            (GRID_X - 4, GRID_Y - 4, board_px_w + 8, board_px_h + 8),
            border_radius=4,
        )

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pre.drawTetrisRect(
                    self.screen,
                    x,
                    y,
                    size=BLOCK_SIZE,
                    offset=6,
                    type=self.board[x][y],
                    grid_start_x=GRID_X,
                    grid_start_y=GRID_Y,
                )

    def draw_current_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if not cell:
                    continue
                bx = self.current_piece.x + x
                by = self.current_piece.y + y
                if by < 0:
                    continue
                pre.drawTetrisRect(
                    self.screen,
                    bx,
                    by,
                    size=BLOCK_SIZE,
                    offset=6,
                    type=self.current_piece.kind,
                    grid_start_x=GRID_X,
                    grid_start_y=GRID_Y,
                )

    def draw_preview_piece(self, piece_kind, box_rect, block_size):
        if piece_kind is None:
            return

        piece = Piece(piece_kind, GRID_WIDTH)
        shape = piece.shape
        shape_w = len(shape[0])
        shape_h = len(shape)

        start_x = box_rect.x + (box_rect.width - shape_w * block_size) // 2
        start_y = box_rect.y + (box_rect.height - shape_h * block_size) // 2

        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if not cell:
                    continue
                pre.drawTetrisRect(
                    self.screen,
                    col_idx,
                    row_idx,
                    size=block_size,
                    offset=max(2, block_size // 5),
                    type=piece_kind,
                    grid_start_x=start_x,
                    grid_start_y=start_y,
                )

    def draw_ui(self):
        board_right = GRID_X + GRID_WIDTH * BLOCK_SIZE

        title = self.font.render("Tetris", True, (240, 240, 240))
        hold_label = self.small_font.render("Saved Piece", True, (220, 220, 220))
        hold_box = pygame.Rect(20, GRID_Y + 40, 140, 140)

        queue_label = self.small_font.render("Next 3", True, (220, 220, 220))
        queue_container = pygame.Rect(board_right + 30, GRID_Y + 40, 170, 390)
        stats_container = pygame.Rect(
            queue_container.x,
            queue_container.bottom + 20,
            queue_container.width,
            170,
        )
        self.pause_button_rect = pygame.Rect(
            queue_container.x,
            stats_container.bottom + 20,
            queue_container.width,
            52,
        )

        self.screen.blit(title, (board_right + 30, GRID_Y - 10))

        self.screen.blit(hold_label, (hold_box.x, hold_box.y - 30))
        pygame.draw.rect(self.screen, (95, 95, 105), hold_box, border_radius=6, width=2)
        self.draw_preview_piece(
            self.saved_piece.kind if self.saved_piece is not None else None,
            hold_box,
            block_size=24,
        )

        self.screen.blit(queue_label, (queue_container.x, queue_container.y - 30))
        pygame.draw.rect(self.screen, (95, 95, 105), queue_container, border_radius=6, width=2)

        next_kinds = self.piece_queue.preview(3)
        slot_height = 120
        for i in range(3):
            slot_rect = pygame.Rect(
                queue_container.x + 15,
                queue_container.y + 10 + i * slot_height,
                queue_container.width - 30,
                slot_height - 10,
            )
            pygame.draw.rect(self.screen, (70, 70, 80), slot_rect, border_radius=4, width=1)
            self.draw_preview_piece(next_kinds[i], slot_rect, block_size=20)

        pygame.draw.rect(self.screen, (95, 95, 105), stats_container, border_radius=6, width=2)
        score_label = self.flashy_label_font.render("SCORE", True, (255, 200, 90))
        score_value = self.flashy_font.render(str(self.score), True, (255, 245, 120))
        lines_label = self.flashy_label_font.render("LINES", True, (140, 220, 255))
        lines_value = self.flashy_font.render(str(self.lines), True, (190, 250, 255))
        level_label = self.flashy_label_font.render("LEVEL", True, (205, 150, 255))
        level_value = self.flashy_font.render(str(self.level), True, (230, 185, 255))

        self.screen.blit(score_label, (stats_container.x + 12, stats_container.y + 8))
        self.screen.blit(score_value, (stats_container.right - score_value.get_width() - 12, stats_container.y + 4))
        self.screen.blit(lines_label, (stats_container.x + 12, stats_container.y + 58))
        self.screen.blit(lines_value, (stats_container.right - lines_value.get_width() - 12, stats_container.y + 54))
        self.screen.blit(level_label, (stats_container.x + 12, stats_container.y + 108))
        self.screen.blit(level_value, (stats_container.right - level_value.get_width() - 12, stats_container.y + 104))

        button_color = (95, 120, 190) if not self.paused else (100, 180, 120)
        pygame.draw.rect(self.screen, button_color, self.pause_button_rect, border_radius=8)
        button_text = "Pause + Controls" if not self.paused else "Resume"
        button_surf = self.small_font.render(button_text, True, (245, 245, 245))
        self.screen.blit(
            button_surf,
            (
                self.pause_button_rect.centerx - button_surf.get_width() // 2,
                self.pause_button_rect.centery - button_surf.get_height() // 2,
            ),
        )

        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            panel_rect = pygame.Rect(GRID_X + 40, GRID_Y + 80, 430, 430)
            pygame.draw.rect(self.screen, (35, 35, 45), panel_rect, border_radius=10)
            pygame.draw.rect(self.screen, (120, 120, 150), panel_rect, width=2, border_radius=10)

            pause_title = self.font.render("Paused - Controls", True, (255, 255, 255))
            self.screen.blit(
                pause_title,
                (panel_rect.centerx - pause_title.get_width() // 2, panel_rect.y + 24),
            )

            controls = [
                "A/D or <-/-> : Move",
                "S or Down     : Soft drop",
                "W or Up       : Rotate",
                "Space         : Hard drop",
                "C/Shift       : Save/Swap",
                "P             : Pause/Resume",
            ]
            for i, text in enumerate(controls):
                surf = self.small_font.render(text, True, (225, 225, 225))
                self.screen.blit(surf, (panel_rect.x + 40, panel_rect.y + 90 + i * 45))

        if self.game_over:
            over = self.font.render("Game Over", True, (255, 120, 120))
            restart = self.small_font.render("Press R to restart", True, (255, 255, 255))
            self.screen.blit(over, (board_right + 30, GRID_Y + 300))
            self.screen.blit(restart, (board_right + 30, GRID_Y + 340))

    def draw(self):
        self.screen.fill((26, 26, 30))
        self.draw_board()
        if not self.game_over and not self.paused:
            self.draw_current_piece()
        self.draw_ui()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
