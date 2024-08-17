class Item:
# https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_name
# https://bulbapedia.bulbagarden.net/wiki/Item

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.id = None
        self.effect = None
        self.use = None # Held, From Bag, In Bag, Trade
        self.sellable = False

