import pygame

def drawBGRect(screen, x, y):
    weight = 2
    pygame.draw.rect(screen, (150, 150, 150), (x, y, 50, 50))
    pygame.draw.line(screen, (0,0,0), (x, y), (x+50, y), weight)
    pygame.draw.line(screen, (0,0,0), (x+50, y), (x+50, y+50), weight)
    pygame.draw.line(screen, (0,0,0), (x+50, y+50), (x, y+50), weight)
    pygame.draw.line(screen, (0,0,0), (x, y+50), (x, y), weight)

def squareColor(type):
    match type:
        case "x":
            color = (155, 155, 155)
        case "l":
            color = (0, 245, 255)
    return color



def drawTetrisRect(screen, x, y, size=40, offset=8, type="x"):
    gridStartX = 30
    gridStartY = 40
    print(f'Size: {size} x: {x} gridStartX {gridStartX}')
    print(f'Size: {size} x: {y} gridStartX {gridStartY}')
    x = (0 + (1*size)*x) + gridStartX
    y = (0 + (1*size)*y) + gridStartY
    base_color = squareColor(type)
    shades = get_beveled_colors(base_color)

    pygame.draw.rect(screen, base_color, (x, y, size, size))
    right_points = [(x+size, y), (x+size, y+size), (x+size-offset, y+size-offset), (x+size-offset,y+offset)]
    bottom_points = [(x, y+size), (x+offset, y+size-offset), (x+size-offset, y+size-offset), (x+size,y+size)]
    left_points = [(x, y), (x+offset, y+offset), (x+offset, y+size-offset), (x,y+size)]
    top_points = [(x, y), (x+offset, y+offset), (x+size-offset, y+offset), (x+size,y)]
    pygame.draw.polygon(screen, shades["right"] , right_points)
    pygame.draw.polygon(screen, shades["bottom"] , bottom_points)
    pygame.draw.polygon(screen, shades["left"] , left_points)
    pygame.draw.polygon(screen, shades["top"] , top_points)

def get_beveled_colors(base_rgb):
    r, g, b = base_rgb
    
    def adjust(color, factor):
        # Multiplies each channel by the factor and clamps between 0-255
        return tuple(max(0, min(255, int(c * factor))) for c in color)

    return {
        "middle": (r, g, b),
        "top":    adjust((r, g, b), 1.30), # Lightest
        "left":   adjust((r, g, b), 1.15), # Lighter
        "right":  adjust((r, g, b), 0.85), # Darker
        "bottom": adjust((r, g, b), 0.60)  # Darkest
    }
