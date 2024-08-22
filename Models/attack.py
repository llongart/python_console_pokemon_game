from constants import ST_NORMAL, ST_CONFUSION
from random import randint

class Attack:

    def __init__(self, name, ztype, category, power, accuracy, pp, stage):
        self.name = name
        self.ztype = ztype
        self.category = category
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.stage = stage
        self.turns_to_execute = 1
    
    def chatter(self, pokemon):
        percentage = 10 
        random_value = randint(0, 10) * 10
        if random_value == percentage and pokemon.current_status == ST_NORMAL:
            pokemon.current_status = ST_CONFUSION
        
        return pokemon