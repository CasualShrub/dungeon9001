import sys
import pygame

from constants import *
from dungeon import *
from player import Player
from enemy import *
from item import Item

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon 9001")
        self.clock = pygame.time.Clock()

        self.regularFont = pygame.font.SysFont("monospace", 18)

        self.startGame()

    def startGame(self):
        self.gameState = EXPLORING
        self.dungeon = Dungeon()
        playerX, playerY = self.dungeon.getPlayerSpawn()
        self.player = Player(playerX, playerY)

        self.cameraX = 0
        self.cameraY = 0 #TODO maybve move camera to its own class? not sure if worth
        self.updateCamera()

        self.enemies = []
        enemyPositions = self.dungeon.enemyPositions
        for enemyX, enemyY in enemyPositions:
            self.enemies.append(Enemy(enemyX, enemyY))
        
        self.currentEnemy = None
    
    
    def move(self, xToAdd, yToAdd):
        newX, newY = self.player.x + xToAdd, self.player.y + yToAdd
        tile = self.dungeon.getTile(newX, newY)
        if tile == WALL:
            return
        
        didCollideWithEnemy = self.isEnemyAt(newX, newY)
        if didCollideWithEnemy:
            enemy = self.getEnemyAtPosition(newX, newY)
            #fight the enemy here TODO
            return
        
        self.player.x = newX
        self.player.y = newY
        self.updateCamera()

        if tile == EXIT:
            self.state = VICTORY
    
    def isEnemyAt(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return True
        else:
            return False
    
    def getEnemyAtPosition(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and e.enemy == y:
                return enemy
        else:
            return None


    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type != pygame.KEYDOWN:
                continue
        
            if self.gameState == EXPLORING:
                if event.key in (pygame.K_UP, pygame.K_w): 
                    self.move(0,-1)
                elif event.key in (pygame.K_DOWN,  pygame.K_s):
                    self.move(0, 1)
                elif event.key in (pygame.K_LEFT,  pygame.K_a):
                    self.move(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d): 
                    self.move( 1, 0)
    
    def renderDungeon(self):
        self.screen.set_clip(pygame.Rect(0, 0, MAP_DISPLAY_WIDTH, SCREEN_HEIGHT))

        #first we have to render the map
        for col in range(MAP_COLUMNS):
            for row in range(MAP_ROWS):
                tileX = self.cameraX + col
                tileY = self.cameraY + row
                tile = self.dungeon.getTile(tileX, tileY)

                #pygame needs to draw the rect thing using top left so we need to mult by each tile size
                left = col * TILE_SIZE
                top = row * TILE_SIZE
                rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)

                if tile == WALL:
                    pygame.draw.rect(self.screen, DARK_GRAY_WALL, rect)
                    pygame.draw.rect(self.screen, DARK_GRAY_WALL_BORDER, rect, 1) #cool border radius parameter!
                elif tile == FLOOR:
                    pygame.draw.rect(self.screen, DARK_BROWN, rect)
                    pygame.draw.rect(self.screen, DARK_BROWN_FLOOR_BORDER, rect, 1)
                elif tile == EXIT:
                    pygame.draw.rect(self.screen, DARK_BROWN, rect)
                    s = self.renderText("X", self.regularFont, YELLOW)
                    self.screen.blit(s, (left + 8, top + 6)) #in pygame we can just render the font first and then blit it somehwere else. my preferred approach

        for enemy in self.enemies:
            enemyColumn = enemy.x - self.cameraX
            enemeyRow = enemy.y - self.cameraY
            if 0 <= enemyColumn < MAP_COLUMNS and 0 <= enemeyRow < MAP_ROWS:
                left = enemyColumn * TILE_SIZE
                top = enemeyRow * TILE_SIZE
                enemySymbol, color = ENEMY_SYMBOLS.get(enemy.name, ("?", RED))
                pygame.draw.rect(self.screen, ENEMY_DARK_RED, (left, top, TILE_SIZE, TILE_SIZE))
                text = self.renderText(enemySymbol, self.regularFont, color)
                self.screen.blit(text, (left + 9, top + 6)) 

        pc = self.player.x - self.cameraX
        pr = self.player.y - self.cameraY
        left = pc * TILE_SIZE
        top = pr * TILE_SIZE
        pygame.draw.rect(self.screen, DARK_BLUE_PLAYER, (left, top, TILE_SIZE, TILE_SIZE))
        text = self.renderText("😎", self.regularFont, BLUE)
        self.screen.blit(text, (left + 8, top + 6))

        self.screen.set_clip(None)

    def render(self):
        self.screen.fill(BLACK)

        self.renderDungeon()

        pygame.display.flip()
    
    def renderText(self, text, font, color):
        return font.render(text, True, color)
    
    def updateCamera(self):
        self.cameraX = self.player.x - MAP_COLUMNS // 2
        self.cameraY = self.player.y - MAP_ROWS // 2

        

    def gameLoop(self):
        while True:
            self.handleEvents()
            self.render()
            self.clock.tick(FPS)



if __name__ == "__main__":
    game = Game()
    game.gameLoop()
