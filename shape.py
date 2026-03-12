import random


SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
}


class Piece:
    def __init__(self, kind: str, grid_width: int = 10):
        self.kind = kind
        self.shape = [row[:] for row in SHAPES[kind]]
        self.reset_position(grid_width)

    def reset_position(self, grid_width: int):
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotated(self):
        return [list(row) for row in zip(*self.shape[::-1])]


class PieceQueue:
    def __init__(self, grid_width: int = 10, preview_count: int = 3):
        self.grid_width = grid_width
        self.preview_count = preview_count
        self.queue = []
        self._bag = []
        self._ensure_queue()

    def _refill_bag(self):
        self._bag = list(SHAPES.keys())
        random.shuffle(self._bag)

    def _next_kind(self):
        if not self._bag:
            self._refill_bag()
        return self._bag.pop()

    def _ensure_queue(self):
        while len(self.queue) < self.preview_count + 1:
            self.queue.append(self._next_kind())

    def pull(self):
        self._ensure_queue()
        kind = self.queue.pop(0)
        self._ensure_queue()
        return Piece(kind, self.grid_width)

    def preview(self, count: int | None = None):
        self._ensure_queue()
        to_show = self.preview_count if count is None else count
        return self.queue[:to_show]
