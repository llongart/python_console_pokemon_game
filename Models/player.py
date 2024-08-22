from constants import TRAINER_BADGES
from Models.bag import Bag
from Models.storage import Storage

class Player:

    def __init__(self, gender, name):
        self.gender = gender
        self.name = name
        self.money = 5000    
        self.money_base = 96
        self.pokemons = []
        self.bag = Bag() 
        self.badges = TRAINER_BADGES
        self.storage = Storage()
