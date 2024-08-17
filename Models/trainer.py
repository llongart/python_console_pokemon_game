class Trainer:

    def __init__(self, gender, name):
        self.gender = gender
        self.name = name
        self.group = None
        self.pokemons = []
        self.items = []
        self.money_base = 50 # https://bulbapedia.bulbagarden.net/wiki/Prize_money