import pygame
import sys
import tetrominoes as t
import prefabs as pre
import shape

# Constants for easy adjustments
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLUE  = (0, 100, 250)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("My Pygame Template")
        self.clock = pygame.time.Clock()
        self.running = True

        # Example player properties
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.speed = 5
        self.blockList = []

    def handle_events(self, x):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Continuous keyboard input (Best for movement)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            return int(x - 1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return int(x + 1)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_pos[1] -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_pos[1] += self.speed
        return x

    def update(self):
        # Add game logic here (collisions, score, etc.)
        pass
    
    def drawShape(self, x, y):
        piece = shape.pieces("l")
        self.createList()
        for i in range(len(piece.pieceShape)):
            for j in range(len(piece.pieceShape[i])):
                self.blockList[i+x][j+y] = piece.pieceShape[i][j]


    def createList(self):
        self.blockList = []
        for i in range(10):
            colList = []
            for j in range(19):
                colList.append("x")
            self.blockList.append(colList)

    def drawGrid(self):
        size = 40
        for i in range(len(self.blockList)):
            for j in range(len(self.blockList[i])):
                pre.drawTetrisRect(self.screen,i,j, type = self.blockList[i][j])
                
    def draw(self):
        self.screen.fill((30, 30, 30)) # Fill background with dark grey
        
        # Draw a simple square to represent the player
        #pygame.draw.rect(self.screen, BLUE, (self.player_pos[0], self.player_pos[1], 50, 50))
        self.drawGrid()
        
        
         # Update the full display Surface to the screen

    def run(self):
        self.createList()
        timer = 0
        x = 4
        y = 0
        while self.running:
            if 0 == timer % 15:
                x = self.handle_events(x)
            self.update()
            self.draw()
            self.drawShape(x, y)
            if 0 == timer % 100:
                y += 1
            timer +=1

            pygame.display.flip()
            self.clock.tick(FPS) # Maintain 60 frames per second

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()