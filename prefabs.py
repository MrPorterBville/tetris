import pygame


def squareColor(type):
    colors = {
        "x": (55, 55, 65),
        "I": (0, 245, 255),
        "O": (255, 215, 0),
        "T": (160, 64, 255),
        "S": (64, 255, 96),
        "Z": (255, 96, 96),
        "J": (75, 120, 255),
        "L": (255, 165, 0),
        # backward compatibility with previous data
        "l": (0, 245, 255),
    }
    return colors.get(type, (200, 200, 200))


def drawTetrisRect(screen, x, y, size=40, offset=8, type="x", grid_start_x=30, grid_start_y=40):
    x = x * size + grid_start_x
    y = y * size + grid_start_y
    base_color = squareColor(type)
    shades = get_beveled_colors(base_color)

    pygame.draw.rect(screen, base_color, (x, y, size, size))
    right_points = [(x + size, y), (x + size, y + size), (x + size - offset, y + size - offset), (x + size - offset, y + offset)]
    bottom_points = [(x, y + size), (x + offset, y + size - offset), (x + size - offset, y + size - offset), (x + size, y + size)]
    left_points = [(x, y), (x + offset, y + offset), (x + offset, y + size - offset), (x, y + size)]
    top_points = [(x, y), (x + offset, y + offset), (x + size - offset, y + offset), (x + size, y)]
    pygame.draw.polygon(screen, shades["right"], right_points)
    pygame.draw.polygon(screen, shades["bottom"], bottom_points)
    pygame.draw.polygon(screen, shades["left"], left_points)
    pygame.draw.polygon(screen, shades["top"], top_points)


def get_beveled_colors(base_rgb):
    r, g, b = base_rgb

    def adjust(color, factor):
        return tuple(max(0, min(255, int(c * factor))) for c in color)

    return {
        "middle": (r, g, b),
        "top": adjust((r, g, b), 1.30),
        "left": adjust((r, g, b), 1.15),
        "right": adjust((r, g, b), 0.85),
        "bottom": adjust((r, g, b), 0.60),
    }
