import sys
import pygame
import random

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

        self.smallFont = pygame.font.SysFont("segoe uiemoji", 14)
        self.regularFont = pygame.font.SysFont("segoe uiemoji", 18)
        self.bigFont = pygame.font.SysFont("segoe uiemoji", 24, bold=True)

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
        self.combatLog   = []
        self.pendingItem = None
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
            self.battle(enemy)
            return
        
        self.player.x = newX
        self.player.y = newY
        self.updateCamera()
        self.enemyMoveStep()

        if tile == EXIT:
            self.gameState = VICTORY
    
    def enemyMoveStep(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for enemy in self.enemies:
            dx = random.choice(directions)[0]
            dy = random.choice(directions)[1]

            targetX = enemy.x + dx
            targetY = enemy.y + dy
            if self.dungeon.getTile(targetX, targetY) == WALL:
                continue
            if self.isEnemyAt(targetX, targetY):
                continue
            enemy.x = targetX
            enemy.y = targetY

    def isEnemyAt(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return True
        else:
            return False
    
    def getEnemyAtPosition(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return enemy
        else:
            return None

    def battle(self, enemy):
        self.gameState = BATTLE
        self.currentEnemy = enemy
        self.combatLog = [
            f"A {enemy.name} blocks your path!",
            f"  Enemy — HP:{enemy.hp}  STR:{enemy.strength}  DEF:{enemy.defense}",
            "Press SPACE to attack, or R to run.",
        ]

    def attack(self):
        damage = self.player.attack()
        damageDealt = self.currentEnemy.takeDamage(damage)
        self.combatLog.append(f"You dealt {damageDealt} damage to the {self.currentEnemy.name}.")

        if not self.currentEnemy.isAlive():
            self.combatLog.append(f"You defeated the {self.currentEnemy.name}!")
            self.enemies.remove(self.currentEnemy)
            self.pendingItem = Item()
            self.combatLog.append(f"You found: {self.pendingItem.name}!")
            self.gameState = CLAIM_ITEM
            return

        incomingDamge = self.currentEnemy.attack()
        damageReceived = self.player.takeDamage(incomingDamge)
        self.combatLog.append(
            f"The {self.currentEnemy.name} hits you for {damageReceived} damage."
        )
        if not self.player.isAlive():
            self.combatLog.append("You have been slain...")
            self.gameState = GAME_OVER

    def run(self):
        if random.random() < 0.5:
            self.combatLog.append("You escaped!")
            self.gameState = EXPLORING
            self.currentEnemy = None
        else:
            incomingDamage = self.currentEnemy.attack()
            damageReceived = self.player.takeDamage(incomingDamage)
            self.combatLog.append(
                f"Failed to escape! The {self.currentEnemy.name} hits for {damageReceived}."
            )
            if not self.player.isAlive():
                self.combatLog.append("You have been slain...")
                self.gameState = GAME_OVER
    
    def collectItem(self):
        if self.pendingItem:
            self.pendingItem.equip(self.player)
            self.pendingItem = None
        self.currentEnemy = None
        self.gameState = EXPLORING

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
            elif self.gameState == BATTLE:
                if event.key == pygame.K_SPACE:
                    self.attack()
                elif event.key == pygame.K_r:
                    self.run()
            elif self.gameState == CLAIM_ITEM:
                if event.key == pygame.K_SPACE:
                    self.collectItem()
            elif self.gameState == GAME_OVER:
                if event.key == pygame.K_RETURN:
                    self.startGame()
    
    def collectItem(self):
        if self.pendingItem:
            self.pendingItem.equip(self.player)
            self.pendingItem = None
        self.currentEnemy = None
        self.gameState = EXPLORING
    
    # this is the logic 
    def canDrawTile(self, targetX, targetY):
        x = self.player.x
        y = self.player.y
        dx = abs(targetX - x)
        dy = abs(targetY - y)

        directionX = 1
        if targetX <= x:
            directionX = -1
        
        directionY = 1
        if targetY <= y:
            directionY = -1

        # used Bresenham's line generation algorithm to help figure out the logic fpr this https://www.geeksforgeeks.org/dsa/bresenhams-line-generation-algorithm/
        stepCount = dx - dy

        while x != targetX or y != targetY:
            errorSpace = 2 * stepCount
            if errorSpace > -dy: #if the error space is large, then we can move horizontal!
                stepCount -= dy
                x += directionX
            if errorSpace < dx: #if the different is small, then we can move vertical!
                stepCount += dx
                y += directionY

            # if we hit a wall just block the vision
            if (x != targetX or y != targetY) and self.dungeon.getTile(x, y) == WALL:
                return False
        return True

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

                distX = abs(tileX - self.player.x)
                distY = abs(tileY - self.player.y)
                inRange = distX + distY <= FOG_RADIUS
                isVisble = inRange and self.canDrawTile(tileX, tileY)

                if not isVisble:
                    pygame.draw.rect(self.screen, BLACK, rect)
                elif tile == WALL:
                    pygame.draw.rect(self.screen, BLACK, rect)
                    pygame.draw.rect(self.screen, DARK_GRAY_WALL_BORDER, rect, 1)
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
            if 0 <= enemyColumn < MAP_COLUMNS and 0 <= enemeyRow < MAP_ROWS and abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y) <= FOG_RADIUS and self.canDrawTile(enemy.x, enemy.y):
                left = enemyColumn * TILE_SIZE
                top = enemeyRow * TILE_SIZE
                enemySymbol, color = ENEMY_SYMBOLS.get(enemy.name, ("?", RED))
                pygame.draw.rect(self.screen, ENEMY_DARK_RED, (left, top, TILE_SIZE, TILE_SIZE))
                text = self.renderText(enemySymbol, self.regularFont, color)
                self.screen.blit(text, (left + 4, top + 6)) 

        pc = self.player.x - self.cameraX
        pr = self.player.y - self.cameraY
        left = pc * TILE_SIZE
        top = pr * TILE_SIZE
        pygame.draw.rect(self.screen, DARK_BLUE_PLAYER, (left, top, TILE_SIZE, TILE_SIZE))
        text = self.renderText("😎", self.regularFont, BLUE)
        self.screen.blit(text, (left + 4, top + 6))

        self.screen.set_clip(None)
    
    def renderBattle(self):
        overlay = pygame.Surface((MAP_DISPLAY_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) #slightly transparent overlay!
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        battleWidth = 620
        battleHeight = 380
        battleX = (MAP_DISPLAY_WIDTH - battleWidth) // 2
        battleY = (SCREEN_HEIGHT - battleHeight) // 2
        pygame.draw.rect(self.screen, (18, 8, 8),  (battleX, battleY, battleWidth, battleHeight))
        pygame.draw.rect(self.screen, RED, (battleX, battleY, battleWidth, battleHeight), 2)

        enemy  = self.currentEnemy
        player  = self.player
        barWidth = battleWidth - 40

        self.screen.blit(
            self.renderText(f"BATTLE: {enemy.name.upper()}", self.bigFont, RED),
            (battleX + 20, battleY + 14)
        )

        enemyY = battleY + 52
        enemyHealthRatio = enemy.hp / enemy.maxHp
        barHeight = 15
        pygame.draw.rect(self.screen, DARK_GRAY_WALL_BORDER, (battleX + 20, enemyY, barWidth, barHeight))
        pygame.draw.rect(self.screen, RED, (battleX + 20, enemyY, int(barWidth * max(0.0, enemyHealthRatio)), barHeight))
        pygame.draw.rect(self.screen, GRAY, (battleX + 20, enemyY, barWidth, barHeight), 1)
        self.screen.blit(
            self.renderText(f"Enemy HP: {enemy.hp}/{enemy.maxHp} STR:{enemy.strength} DEF:{enemy.defense}", self.smallFont, WHITE),
            (battleX + 24, enemyY + 1)
        )

        playerY = enemyY + 28
        playerRatio  = player.hp / player.max_hp

        # TODO move these to their own function later like draw bbar or something
        pygame.draw.rect(self.screen, DARK_GRAY_WALL_BORDER, (battleX + 20, playerY, barWidth, barHeight))
        pygame.draw.rect(self.screen, self.getHpColor(playerRatio), (battleX + 20, playerY, int(barWidth * max(0.0, playerRatio)), barHeight))
        pygame.draw.rect(self.screen, GRAY, (battleX + 20, playerY, barWidth, barHeight), 1)
        self.screen.blit(
            self.renderText(f"Your  HP: {player.hp}/{player.max_hp}   STR:{player.strength}  DEF:{player.defense}", self.smallFont, WHITE),
            (battleX + 24, playerY + 1)
        )

        combatLogY = battleY + 112
        pygame.draw.line(self.screen, GRAY, (battleX + 10, combatLogY - 5), (battleX + battleWidth - 10, combatLogY - 5))
        #lets only get the most recent 10 logs
        visibleLogs = self.combatLog[-9:]
        for i, line in enumerate(visibleLogs):
            if i == len(visibleLogs) - 1:
                color = YELLOW 
            else: 
                color = WHITE
            
            self.screen.blit(self.renderText(line, self.smallFont, color), (battleX + 20, combatLogY + i * 22))

        controlY = battleY + battleHeight - 36
        pygame.draw.line(self.screen, GRAY, (battleX + 10, controlY - 5), (battleX + battleWidth - 10, controlY - 5))
        self.screen.blit(self.renderText("[SPACE] Attack          [R] Run", self.regularFont, YELLOW),
            (battleX + 20, controlY)
        )

    def renderItemScreen(self):
        overlay = pygame.Surface((MAP_DISPLAY_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        panelWidth = 500
        panelHeight = 300
        panelX = (MAP_DISPLAY_WIDTH - panelWidth) // 2
        panelY = (SCREEN_HEIGHT - panelHeight) // 2
        pygame.draw.rect(self.screen, DARK_GRAY_WALL_BORDER, (panelX, panelY, panelWidth, panelHeight))
        pygame.draw.rect(self.screen, YELLOW, (panelX, panelY, panelWidth, panelHeight), 2)

        item = self.pendingItem
        self.screen.blit(self.renderText("ITEM FOUND!", self.bigFont, YELLOW), (panelX + 20, panelY + 16))
        self.screen.blit(self.renderText(item.name, self.bigFont, WHITE), (panelX + 20, panelY + 52))
        self.screen.blit(self.renderText(item.desc, self.regularFont, GRAY), (panelX + 20, panelY + 86))

        y = panelY + 124
        for text, positive in item.getStatBonusString():
            if positive:
                color = GREEN 
            else:
                color = RED
            self.screen.blit(self.renderText(text, self.regularFont, color), (panelX + 20, y))
            y += 28

        cy = panelY + panelHeight - 36
        pygame.draw.line(self.screen, GRAY, (panelX + 10, cy - 5), (panelX + panelWidth - 10, cy - 5))
        self.screen.blit(self.renderText("[SPACE] Collect Item", self.regularFont, YELLOW), (panelX + 20, cy))

    
    def renderGameEnd(self):
        self.screen.fill(BLACK)
        position = SCREEN_WIDTH // 2
        titleText = self.renderText("YOU DIED", self.bigFont, RED)
        titlePos = position - titleText.get_width() // 2
        self.screen.blit(titleText, (titlePos, 220))

        descText = self.renderText("Press ENTER to play again", self.regularFont, WHITE)
        descPos = position - descText.get_width() // 2
        self.screen.blit(descText, (descPos, 270))
    
    
    def renderSideMenu(self):
        startX = MAP_DISPLAY_WIDTH #i'm defining start x is the right edge of the map,, where the sidebar begins
        pygame.draw.rect(self.screen, REALLY_DARK_BLUE, (startX, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(self.screen, GRAY, (startX, 0), (startX, SCREEN_HEIGHT), 2)

        x = startX + 10
        y = 12 # increase y to move to draw the next row

        self.screen.blit(self.renderText("DUNGEON 9001", self.bigFont, YELLOW), (x, y));
        y += 30

        pygame.draw.line(self.screen, GRAY, (startX + 5, y), (SCREEN_WIDTH - 5, y));
        y += 10

        p = self.player
        barWidth = SIDEBAR_WIDTH - 20
        barHeight = 17

        self.screen.blit(self.renderText("HP", self.regularFont, WHITE), (x, y));
        y += 22
        ratio = p.hp / p.max_hp

        pygame.draw.rect(self.screen, DARK_GRAY_WALL_BORDER, (x, y, barWidth, barHeight))
        pygame.draw.rect(self.screen, self.getHpColor(ratio), (x, y, int(barWidth * max(0.0, ratio)), barHeight))
        pygame.draw.rect(self.screen, GRAY, (x, y, barWidth, barHeight), 1)
        lbl = self.renderText(f"{p.hp}/{p.max_hp}", self.regularFont, WHITE)
        self.screen.blit(lbl, (x + 4, y + 1)); y += 24

        self.screen.blit(self.renderText(f"STR: {p.strength}", self.regularFont, ORANGE), (x, y));
        y += 26
        self.screen.blit(self.renderText(f"DEF: {p.defense}",  self.regularFont, BLUE),   (x, y));
        y += 30

        pygame.draw.line(self.screen, GRAY, (startX + 5, y), (SCREEN_WIDTH - 5, y));
        y += 10

        count = len(self.enemies)
            
        self.screen.blit(self.renderText(f"Enemies left on this floor: {count}", self.smallFont, RED), (x, y));
        y += 20
        self.screen.blit(self.renderText("Find X to escape!",  self.smallFont, GRAY), (x, y));
        y += 22

        pygame.draw.line(self.screen, GRAY, (startX + 5, y), (SCREEN_WIDTH - 5, y));
        y += 10

        self.screen.blit(self.renderText("ITEMS:", self.regularFont, WHITE), (x, y));
        y += 22
        if p.items:
            for name in p.items[-8:]:
                txt = name if len(name) <= 14 else name[:13] + "…"
                self.screen.blit(self.renderText(f"- {txt}", self.smallFont, WHITE), (x, y))
                y += 18
        else:
            self.screen.blit(self.renderText("(none)", self.smallFont, GRAY), (x, y));
            y += 18

        y = SCREEN_HEIGHT - 100
        pygame.draw.line(self.screen, GRAY, (startX + 5, y), (SCREEN_WIDTH - 5, y));
        y += 8
        for line in ["WASD / Arrows: move", "SPACE: attack", "R: run from battle"]:
            self.screen.blit(self.renderText(line, self.smallFont, DARK_GRAY_WALL), (x, y));
            y += 18

    def render(self):
        self.screen.fill(BLACK)

        if self.gameState == GAME_OVER: 
            self.renderGameEnd()
        else:
            self.renderDungeon()
            self.renderSideMenu()
            if self.gameState == BATTLE:
                self.renderBattle()
            elif self.gameState == CLAIM_ITEM:
                self.renderItemScreen()

        pygame.display.flip()
    
    def renderText(self, text, font, color):
        return font.render(text, True, color)
    
    def updateCamera(self):
        self.cameraX = self.player.x - MAP_COLUMNS // 2
        self.cameraY = self.player.y - MAP_ROWS // 2

    def getHpColor(self, ratio):
        if ratio > 0.5: 
            return GREEN
        elif ratio > 0.25: 
            return ORANGE
        else:
            return RED

    def gameLoop(self):
        while True:
            self.handleEvents()
            self.render()
            self.clock.tick(FPS)



if __name__ == "__main__":
    game = Game()
    game.gameLoop()
