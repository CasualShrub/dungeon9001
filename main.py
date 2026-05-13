import sys
import pygame

from constants import *
from dungeon import *
from player import Player
from enemy import Enemy
from item import Item

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon 9001")
        self.clock = pygame.time.Clock()

        self.startGame()

    def startGame(self):
        self.gameState = EXPLORING
        self.dungeon = Dungeon()
        playerX, playerY = self.dungeon.getPlayerSpawn()
        self.player = Player(playerX, playerY)

        self.enemies = []
        enemyPositions = self.dungeon.enemy_positions4
        for enemyX, enemyY in enemyPositions:
            self.enemies.append(Enemy(ex, ey))
        
        self.currentEnemy = None
    
    
    def move(self, xToAdd, yToAdd):
        newX, newY = self.player.x + xToAdd, self.player.y + yToAdd
        tile = self.dungeon.get_tile(newX, newY)
        if tile == WALL:
            return
        
        didCollideWithEnemy = self.isEnemyAt(newX, newY)
        if didCollideWithEnemy:
            enemy = self.getEnemyAtPosition(newX, newY)
            self._start_battle(enemy)
            return
        
        self.player.x = newX
        self.player.y = newY

        if tile == EXIT:
            self.state = VICTORY
    
    def isEnemyAt(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and e.enemy == y:
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
        
            if self.state == EXPLORING:
                if event.key in (pygame.K_UP, pygame.K_w): 
                    self.move(0,-1)
                elif event.key in (pygame.K_DOWN,  pygame.K_s):
                    self.move(0, 1)
                elif event.key in (pygame.K_LEFT,  pygame.K_a):
                    self.move(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d): 
                    self.move( 1, 0)
    
    def renderDungeon():
        #TODO draw the map tiles
        pass

    def render(self):
        self.screen.fill(BLACK)

        self.renderDungeon()

    def gameLoop(self):
        while True:
            self.handleEvents()
            self.draw()
            self.clock.tick(FPS)



if __name__ == "__main__":
    game = Game()
    game.gameLoop()
