import random

ENEMY_TYPES = [
    {"name": "Slime", "hp": 12, "strength": 4, "defense": 1},
    {"name": "Goblin", "hp": 20, "strength": 6, "defense": 2},
    {"name": "Orc", "hp": 30, "strength": 8, "defense": 3},
    {"name": "Troll", "hp": 45, "strength": 11, "defense": 4},
    {"name": "Dragon", "hp": 60, "strength": 15, "defense": 6},
]

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        enemyData = random.choice(ENEMY_TYPES) #for sake of app simplicity, let's just randomize type on creation
        self.name = enemyData["name"]
        self.maxHp = enemyData["hp"]
        self.hp = enemyData["hp"]
        self.strength = enemyData["strength"]
        self.defense = enemyData["defense"]

    def attack(self):
        roll = random.randint(-1, 2)
        return max(1, self.strength + roll)

    def takeDamage(self, incoming):
        damage = max(1, incoming - self.defense)
        self.hp -= damage
        return damage

    def isAlive(self):
        return self.hp > 0