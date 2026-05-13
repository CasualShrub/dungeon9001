import random
from constants import MAP_WIDTH, MAP_HEIGHT

WALL = 0
FLOOR = 1
EXIT = 2

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getCenterTile(self):
        centerX = self.x + self.width//2
        centerY = self.y + self.height//2
        return (centerX,centerY)

    def doesOverlap(self, other):
        if self.x <= other.x + other.width and self.x + self.width >= other.x and self.y <= other.y + other.height and self.y + self.height >= other.y:
            return True
        else:
            return False


class Dungeon:
    def __init__(self):
        self.tiles = []
        for x in range(MAP_WIDTH):
            column = []
            for y in range(MAP_HEIGHT):
                column.append(WALL)
            self.tiles.append(column)
        self.rooms = []
        self.enemyPositions = []
        self.exitPosition = None
        self.createDungeon()

    def createDungeon(self):
        maxRooms = 12
        minRoomSize = 4
        maxRoomSize = 10

        #maybemove thse magioc numbers to constnants?
        for _ in range(60):
            w = random.randint(minRoomSize, maxRoomSize)
            h = random.randint(minRoomSize, maxRoomSize)
            x = random.randint(1, MAP_WIDTH - w - 1)
            y = random.randint(1, MAP_HEIGHT - h - 1)
            newRoom = Room(x, y, w, h)

            if any(newRoom.doesOverlap(r) for r in self.rooms):
                continue

            self.drawRoom(newRoom)

            if self.rooms:
                self.drawPath(self.rooms[-1].getCenterTile(), newRoom.getCenterTile())

            self.rooms.append(newRoom)
            if len(self.rooms) >= maxRooms:
                break
        
        if not self.rooms:
            return

        centerX, CenterY = self.rooms[-1].getCenterTile()
        self.tiles[centerX][CenterY] = EXIT
        self.exitPosition = (centerX, CenterY)

        for room in self.rooms:
            enemyCount = random.randint(1, 3) #should probably move this to cosntants as well ?
            for counter in range(enemyCount):
                x = random.randint(room.x + 1, room.x + room.width - 2)
                y = random.randint(room.y + 1, room.y + room.height - 2)
                if (x, y) != self.exitPosition and (x, y) not in self.enemyPositions:
                    self.enemyPositions.append((x, y))

    # basically here I just want to make a rect of the tiles a floor tile
    def drawRoom(self, room):
        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                self.tiles[x][y] = FLOOR

    def drawPath(self, start, end):
        x1, y1 = start
        x2, y2 = end

        # this was a suggestion made by gemini! flip a coin to determine how the path should bend.
        # I decided to go with heads (true) for horizontal first then vertical. 
        if random.random() < 0.5: 
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.tiles[x][y1] = FLOOR
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.tiles[x2][y] = FLOOR
        else:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.tiles[x1][y] = FLOOR
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.tiles[x][y2] = FLOOR

    def getTile(self, x, y):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            return self.tiles[x][y]
        else:
            return WALL
        
    def getPlayerSpawn(self):
        if self.rooms:
            return self.rooms[0].getCenterTile()
        else:
            return (0, 0)
