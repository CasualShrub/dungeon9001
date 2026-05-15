import random

ITEM_POOL = [
    {"name": "Tiny Dagger", "str": 2, "def": 0, "hp": 0, "desc": "Teensy weensy but not nothing!"},
    {"name": "Leather Armor", "str": 0, "def": 2, "hp": 0, "desc": "Classic adventurer's gear."},
    {"name": "Health Potion", "str": 0, "def": 0, "hp": 10, "desc": "Restores some HP."},
    {"name": "Battle Axe", "str": 4, "def": 0, "hp": 0, "desc": "It's a bit too heavy."},
    {"name": "Iron Shield", "str": 0, "def": 3, "hp": 0, "desc": "A respectable buckler."},
    {"name": "Elixir", "str": 1, "def": 1, "hp": 5, "desc": "A potion that makes you stronger."},
    {"name": "Pythonic Blade", "str":8, "def": 2, "hp": 0, "desc": "A blade once wielded by the cult of Python."},
    {"name": "The Platemail of Karlos", "str": 0, "def": 6, "hp": 0, "desc": "Impenetrable plated armor once wielded by Karlos the dragon-slayer."},
    {"name": "The Power Ring of Atif","str": 6, "def": -2, "hp": 5, "desc": "A ring once worn by the legendary wizard Atif."},
    {"name": "The Greatsword of Armin","str": 4, "def": 2, "hp": 0, "desc": "An extremely large blade once wielded by Armin the hero"},
]

class Item:
    def __init__(self):
        data = random.choice(ITEM_POOL)
        self.name = data["name"]
        self.str_bonus = data["str"]
        self.def_bonus = data["def"]
        self.hp_bonus  = data["hp"]
        self.desc = data["desc"]

    def equip(self, player):
        player.strength += self.str_bonus
        player.defense += self.def_bonus
        player.max_hp += self.hp_bonus
        player.hp += self.hp_bonus
        player.items.append(self.name)
    
    def getStatBonusString(self):
        output = [] #this ones a list of tuples, the other boolean if its negative 
        if self.str_bonus != 0:
            if self.str_bonus > 0:
                sign = "+"
            else:
                sign = "-"
            output.append((f"STR  {sign}{self.str_bonus}", self.str_bonus > 0))
        if self.def_bonus != 0:
            if self.def_bonus > 0:
                sign = "+"
            else:
                sign = "-"
            output.append((f"DEF  {sign}{self.def_bonus}", self.def_bonus > 0))
        if self.hp_bonus != 0:
            if self.hp_bonus > 0:
                sign = "+"
            else:
                sign = "-"
            output.append((f"HP   {sign}{self.hp_bonus}", self.hp_bonus > 0))
        return output