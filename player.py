import random

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_hp = 30
        self.hp = 30
        self.strength = 8
        self.defense = 3
        self.items = []

    def attack(self):
        bonusDmg = random.randint(-2, 2)
        return max(1, self.strength + bonusDmg)

    def takeDamage(self, incomingDamage):
        reduction = self.defense + random.randint(-1, 1)
        damage = max(1, incomingDamage - reduction)
        self.hp -= damage
        return damage #todo maybe also output the reduction?

    def isAlive(self):
        return self.hp > 0