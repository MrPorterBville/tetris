import pygame

class tetrominoe:



    def __init__(self, ):
        pass
        

    def drawShape(self, screen, color, x, y):
        pygame.draw.rect(screen, color, (x, y, 50, 50))
        pygame.draw.rect(screen, color, (x+50, y, 50, 50))
        pygame.draw.rect(screen, color, (x, y+50, 50, 50))
        pygame.draw.rect(screen, color, (x+50, y+50, 50, 50))