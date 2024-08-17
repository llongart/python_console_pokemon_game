from constants import *
from Models.ui import *
from Models.player import *
from Models.pokemon import *
from os import system

class Bag:

    def __init__(self):
        self.items = []
        self.medicine = []
        self.tm_hm = []
        self.berries = []
        self.key_items = []
        self.free_space = []

# MEDICINE
    # Potion
    def potion(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 20
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]

        for item in self.medicine:
            if item[NAME] == "Potion":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Potion on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
    
        return pokemon
    
    # Super Potion
    def super_potion(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1
        
        if check:
            return 0

        pokemon.current_hp += 50
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]     

        for item in self.medicine:
            if item[NAME] == "Super Potion":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Super Potion on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon    

    # Hyper Potion
    def hyper_potion(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 200
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]     

        for item in self.medicine:
            if item[NAME] == "Hyper Potion":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Hyper Potion on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon

    # Max Potion
    def max_potion(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp = pokemon.stats[HP]     

        for item in self.medicine:
            if item[NAME] == "Max Potion":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Max Potion on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon

    # Antidote
    def antidote(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status not in (ST_POISONED, ST_BADLYPOISON):
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        for item in self.medicine:
            if item[NAME] == "Antidote":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        pokemon.current_status = ST_NORMAL
        UI().delay_print(player.name + " used an Antidote on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been cured of poisoning!")
            
        
        return pokemon

    # Burn Heal
    def burn_heal(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_BURNED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        for item in self.medicine:
            if item[NAME] == "Burn Heal":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        pokemon.current_status = ST_NORMAL
        UI().delay_print(player.name + " used a Burn Heal on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been cured of burning!")

        return pokemon

    # Ice Heal
    def ice_heal(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_FREEZED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        for item in self.medicine:
            if item[NAME] == "Ice Heal":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        pokemon.current_status = ST_NORMAL
        UI().delay_print(player.name + " used an Ice Heal on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been cured of freezing!")            
        
        return pokemon

    # Awakening
    def awakening(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_SLEEP:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        for item in self.medicine:
            if item[NAME] == "Awakening":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        pokemon.current_status = ST_NORMAL
        UI().delay_print(player.name + " used an Awakening on " + pokemon.name)
        UI().delay_print(pokemon.name + " has woken up!")            

        return pokemon 

                      
    # Parlyz Heal
    def parlyz_heal(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_PARALYZED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        for item in self.medicine:
            if item[NAME] == "Parlyz Heal":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        pokemon.current_status = ST_NORMAL
        UI().delay_print(player.name + " used a Parlyz Heal on " + pokemon.name)
        UI().delay_print(pokemon.name + " is not paralyzed!")            

        return pokemon  

    # Full Restore
    def full_restore(self, player, pokemon: Pokemon, check: bool):
        status = (ST_POISONED, ST_BADLYPOISON, ST_BURNED, ST_FREEZED, ST_SLEEP, ST_PARALYZED, ST_CONFUSION)

        if pokemon.current_hp >= pokemon.stats[HP] or pokemon.current_status not in status:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp = pokemon.stats[HP]

        if pokemon.current_status in status:
            pokemon.current_status = ST_NORMAL

        for item in self.medicine:
            if item[NAME] == "Full Restore":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        UI().delay_print(player.name + " used a Full Restore on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been fully cured!")
        
        return pokemon

    # Full Heal
    def full_heal(self, player, pokemon: Pokemon, check: bool):
        status = (ST_POISONED, ST_BADLYPOISON, ST_BURNED, ST_FREEZED, ST_SLEEP, ST_PARALYZED, ST_CONFUSION)

        if pokemon.current_status not in status:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for item in self.medicine:
            if item[NAME] == "Full Heal":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        UI().delay_print(player.name + " used a Full Heal on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been fully healed!")
        
        return pokemon

    # Revive
    def revive(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_FAINTED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp = int(pokemon.stats[HP] / 2)
        pokemon.current_status = ST_NORMAL

        for item in self.medicine:
            if item[NAME] == "Revive":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        UI().delay_print(player.name + " used a Revive on " + pokemon.name)
        UI().delay_print(pokemon.name + " has revived!")
        
        return pokemon

    # Max Revive
    def max_revive(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_FAINTED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp = pokemon.stats[HP]
        pokemon.current_status = ST_NORMAL

        for item in self.medicine:
            if item[NAME] == "Max Revive":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        UI().delay_print(player.name + " used a Max Revive on " + pokemon.name)
        UI().delay_print(pokemon.name + " has revived!")
        
        return pokemon

    # Fresh Water
    def fresh_water(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 50
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]     

        for item in self.medicine:
            if item[NAME] == "Fresh Water":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Fresh Water on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon    

    # Soda pop
    def soda_pop(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0
        
        pokemon.current_hp += 60
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]     

        for item in self.medicine:
            if item[NAME] == "Soda Pop":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Soda Pop on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon 

    # Lemonade
    def lemonade(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 80
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]     

        for item in self.medicine:
            if item[NAME] == "Lemonade":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Lemonade on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon

    # Moomoo Milk
    def moomoo_milk(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 100
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]     

        for item in self.medicine:
            if item[NAME] == "Moomoo Milk":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Moomoo Milk on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon      

    # Energy Powder
    def energy_powder(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 50
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]     

        if pokemon.friendship in range(0, 200):
            pokemon.friendship -= 5
        elif pokemon.friendship in range(200, 256):
            pokemon.friendship -= 10

        for item in self.medicine:
            if item[NAME] == "Energy Powder":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Energy Powder on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon 

    # Energy Root
    def energy_root(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 200
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]     

        if pokemon.friendship in range(0, 200):
            pokemon.friendship -= 10
        elif pokemon.friendship in range(200, 256):
            pokemon.friendship -= 15

        for item in self.medicine:
            if item[NAME] == "Energy Root":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Energy Root on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon         

    # Heal Powder
    def heal_powder(self, player, pokemon: Pokemon, check: bool):
        status = (ST_POISONED, ST_BADLYPOISON, ST_BURNED, ST_FREEZED, ST_SLEEP, ST_PARALYZED, ST_CONFUSION)

        if pokemon.current_status not in status:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        if pokemon.friendship in range(0, 200):
            pokemon.friendship -= 5
        elif pokemon.friendship in range(200, 256):
            pokemon.friendship -= 10

        for item in self.medicine:
            if item[NAME] == "Heal Powder":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Heal Powder on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        
        return pokemon

    # Revival Herb
    def revival_herb(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_FAINTED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp = pokemon.stats[HP]
        pokemon.current_status = ST_NORMAL

        if pokemon.friendship in range(0, 200):
            pokemon.friendship -= 15
        elif pokemon.friendship in range(200, 256):
            pokemon.friendship -= 20

        for item in self.medicine:
            if item[NAME] == "Revival Herb":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Revival Herb on " + pokemon.name)
        UI().delay_print(pokemon.name + " has revived!")
        
        return pokemon
    
    # Ether
    def ether(self, player, pokemon: Pokemon, check: bool):
        # Get attack list from db
        try:
            with open(path_attacks, 'r') as attacks:
                content = attacks.read()
                db_attack_list = loads(content) 
        except Exception:
                db_attack_list = None 
        
        # system('cls')
        i = 1
        for move in pokemon.attacks:
            formated_string = "{0}. {1} ({2}/{3})".format(str(i), move.name, str(move.pp), str(db_attack_list[move.name][PP]))
            print(formated_string)
            i += 1
        
        print("Or type 'Q' or 'ESC' to exit...")
        
        answer = None
        while answer not in range(i):
            answer = input("Select a move: ")
            if not answer.isnumeric() and str(answer).upper() in ['Q', 'ESC']:
                return None
                
            if answer.isnumeric():      

                move = pokemon.attacks[int(answer) - 1]
                db_move = db_attack_list[move.name]   

                if move.pp == int(db_move[PP]):
                    UI().delay_print("Would have no effect")
                    answer = None
                else:
                    break
               
        move.pp += 10
        if int(move.pp) >= int(db_move[PP]):
            move.pp = int(db_move[PP])        

        for item in self.medicine:
            if item[NAME] == "Ether":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used an Ether on " + pokemon.name)
        UI().delay_print("10 PP has been restored from " + move.name)

        return pokemon

    # Max Ether
    def max_ether(self, player, pokemon: Pokemon, check: bool):
        # Get attack list from db
        try:
            with open(path_attacks, 'r') as attacks:
                content = attacks.read()
                db_attack_list = loads(content) 
        except Exception:
                db_attack_list = None 
        
        # print moves from pokemon
        i = 1
        for move in pokemon.attacks:
            formated_string = "{0}. {1} ({2}/{3})".format(str(i), move.name, str(move.pp), str(db_attack_list[move.name][PP]))
            print(formated_string)
            i += 1
        
        print("Or type 'Q' or 'ESC' to exit...")
        
        answer = None
        while answer not in range(i):
            answer = input("Select a move: ")
            if not answer.isnumeric() and str(answer).upper() in ['Q', 'ESC']:
                return None
                
            if answer.isnumeric():      

                move = pokemon.attacks[int(answer) - 1]
                db_move = db_attack_list[move.name]   

                if move.pp == int(db_move[PP]):
                    UI().delay_print("Would have no effect")
                    answer = None
                else:
                    break
               
        move.pp = int(db_move[PP])

        for item in self.medicine:
            if item[NAME] == "Max Ether":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used an Max Ether on " + pokemon.name)
        UI().delay_print("All PP has been restored from " + move.name)

        return pokemon

    
    # Elixir
    def elixir(self, player, pokemon: Pokemon, check: bool):
        # Get attack list from db
        try:
            with open(path_attacks, 'r') as attacks:
                content = attacks.read()
                db_attack_list = loads(content) 
        except Exception:
                db_attack_list = None 

        counter = 0
        for move in pokemon.attacks:
            db_move = db_attack_list[move.name]
            if int(move.pp) >= int(db_move[PP]):
                counter += 1
            elif not check:
                move.pp += 10

                if int(move.pp) >= int(db_move[PP]):
                    move.pp = int(db_move[PP])

        if counter == len(pokemon.attacks):
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        for item in self.medicine:
            if item[NAME] == "Elixir":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used an Ether on " + pokemon.name)
        UI().delay_print("10 PP has been restored from all " + pokemon.name + "'s moves")

        return pokemon

    # Max Elixir
    def max_elixir(self, player, pokemon: Pokemon, check: bool):
        # Get attack list from db
        try:
            with open(path_attacks, 'r') as attacks:
                content = attacks.read()
                db_attack_list = loads(content) 
        except Exception:
                db_attack_list = None 

        counter = 0
        for move in pokemon.attacks:
            db_move = db_attack_list[move.name]
            if int(move.pp) >= int(db_move[PP]):
                counter += 1
            elif not check:
                move.pp = int(db_move[PP])

        if counter == len(pokemon.attacks):
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        for item in self.medicine:
            if item[NAME] == "Max Elixir":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used an Max Elixir on " + pokemon.name)
        UI().delay_print("All PP has been restored from " + pokemon.name + "'s moves")

        return pokemon     

    # Lava Cookie
    def lava_cookie(self, player, pokemon: Pokemon, check: bool):
        status = (ST_POISONED, ST_BADLYPOISON, ST_BURNED, ST_FREEZED, ST_SLEEP, ST_PARALYZED, ST_CONFUSION)

        if pokemon.current_status not in status:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for item in self.medicine:
            if item[NAME] == "Lava Cookie":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        UI().delay_print(player.name + " used a Lava Cookie on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been fully cured!")
        
        return pokemon  

    # Berry Juice
    def berry_juice(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 20
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]

        for item in self.medicine:
            if item[NAME] == "Berry Juice":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Berry Juice on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
    
        return pokemon        

    # Old Gateau
    def old_gateau(self, player, pokemon: Pokemon, check: bool):
        status = (ST_POISONED, ST_BADLYPOISON, ST_BURNED, ST_FREEZED, ST_SLEEP, ST_PARALYZED, ST_CONFUSION)

        if pokemon.current_status not in status:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for item in self.medicine:
            if item[NAME] == "Old Gateau":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        UI().delay_print(player.name + " used an Old Gateau on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been fully cured!")
        
        return pokemon 

    # Sweet Heart
    def sweet_heart(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 20
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]

        for item in self.medicine:
            if item[NAME] == "Sweet Heart":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Sweet Heart on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
    
        return pokemon   

    # Rare Candy Bar
    def rare_candy_bar(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp >= pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_hp += 20
        if pokemon.current_hp > pokemon.stats[HP]:
            pokemon.current_hp = pokemon.stats[HP]

        for item in self.medicine:
            if item[NAME] == "Rare Candy Bar":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)

        UI().delay_print(player.name + " used a Rare Candy Bar on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
    
        return pokemon

    # Casteliacone
    def casteliacone(self, player, pokemon: Pokemon, check: bool):
        status = (ST_POISONED, ST_BADLYPOISON, ST_BURNED, ST_FREEZED, ST_SLEEP, ST_PARALYZED, ST_CONFUSION)

        if pokemon.current_status not in status:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for item in self.medicine:
            if item[NAME] == "Casteliacone":
                item[QUANTITY] -= 1
                if item[QUANTITY] == 0:
                    self.medicine.remove(item)            

        UI().delay_print(player.name + " used an Casteliacone on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been fully cured!")

        return pokemon

# BERRIES
    # Cheri Berry
    def cheri_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_PARALYZED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for berry in self.berries:
            if berry[NAME] == "Cheri Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)            

        UI().delay_print(player.name + " used a Cheri Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " is no longer paralyzed!") 

        return pokemon

    # Chesto Berry
    def chesto_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_SLEEP:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for berry in self.berries:
            if berry[NAME] == "Chesto Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)            

        UI().delay_print(player.name + " used a Chesto Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " has woken up!") 

        return pokemon

    # Pecha Berry
    def chesto_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status not in (ST_POISONED, ST_BADLYPOISON):
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for berry in self.berries:
            if berry[NAME] == "Pecha Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)            

        UI().delay_print(player.name + " used a Pecha Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been cured from poisoning!") 

        return pokemon        

    # Rawst Berry
    def rawst_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_BURNED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for berry in self.berries:
            if berry[NAME] == "Rawst Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)            

        UI().delay_print(player.name + " used a Rawst Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been cured from burning!") 

        return pokemon     

    # Aspear Berry
    def aspear_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_FREEZED:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for berry in self.berries:
            if berry[NAME] == "Aspear Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)            

        UI().delay_print(player.name + " used an Aspear Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " is no longer freezed!") 

        return pokemon
    
    # Leppa Berry
    # TODO SEARCH MORE FROM LEPPA BERRY
    def leppa_berry(self, player, pokemon: Pokemon, check: bool):
        # Get attack list from db
        try:
            with open(path_attacks, 'r') as attacks:
                content = attacks.read()
                db_attack_list = loads(content) 
        except Exception:
                db_attack_list = None 
        
        # system('cls')
        i = 1
        for move in pokemon.attacks:
            formated_string = "{0}. {1} ({2}/{3})".format(str(i), move.name, str(move.pp), str(db_attack_list[move.name][PP]))
            print(formated_string)
            i += 1
        
        print("Or type 'Q' or 'ESC' to exit...")
        
        answer = None
        while answer not in range(i):
            answer = input("Select a move: ")
            if not answer.isnumeric() and str(answer).upper() in ['Q', 'ESC']:
                return None
                
            if answer.isnumeric():      

                move = pokemon.attacks[int(answer) - 1]
                db_move = db_attack_list[move.name]   

                if move.pp == int(db_move[PP]):
                    UI().delay_print("Would have no effect")
                    answer = None
                else:
                    break
               
        move.pp += 10
        if int(move.pp) >= int(db_move[PP]):
            move.pp = int(db_move[PP])        

        for berry in self.berries:
            if berry[NAME] == "Leppa Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)

        UI().delay_print(player.name + " used a Leppa Berry on " + pokemon.name)
        UI().delay_print("10 PP has been restored from " + move.name)

        return pokemon
    
    # Oran Berry
    def oran_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp == pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0
                
        pokemon.current_hp += 10
        if pokemon.current_hp >= pokemon.stats[HP]:
            pokemon.current_hp == pokemon.stats[HP]       

        for berry in self.berries:
            if berry[NAME] == "Oran Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)

        UI().delay_print(player.name + " used an Oran Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        return pokemon

    # Persim Berry
    def persim_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_status != ST_CONFUSION:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for berry in self.berries:
            if berry[NAME] == "Persim Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)            

        UI().delay_print(player.name + " used a Persim Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " is no longer confused!") 

        return pokemon
    
    
    # Lum Berry
    def lum_berry(self, player, pokemon: Pokemon, check: bool):
        status = (ST_POISONED, ST_BADLYPOISON, ST_FREEZED, ST_PARALYZED, ST_SLEEP, ST_CONFUSION)
        if pokemon.current_status not in status:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0

        pokemon.current_status = ST_NORMAL

        for berry in self.berries:
            if berry[NAME] == "Lum Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)            

        UI().delay_print(player.name + " used a Lum Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " has been fully cured!") 

        return pokemon
    
    # Sitrus Berry
    def sitrus_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.current_hp == pokemon.stats[HP]:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0
                
        pokemon.current_hp += int(pokemon.stats[HP] / 4)
        if pokemon.current_hp >= pokemon.stats[HP]:
            pokemon.current_hp == pokemon.stats[HP]       

        for berry in self.berries:
            if berry[NAME] == "Sitrus Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)

        UI().delay_print(player.name + " used an Sitrus Berry on " + pokemon.name)
        UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
        return pokemon
    
    # Razz Berry
    def razz_berry(self, player, pokemon: Pokemon, check: bool):
        if pokemon.master != None:
            UI().delay_print("Would have no effect")
            return -1

        if check:
            return 0
        
        pokemon.catch_rate = int(pokemon.catch_rate * 1.5)
        
        for berry in self.berries:
            if berry[NAME] == "Razz Berry":
                berry[QUANTITY] -= 1
                if berry[QUANTITY] == 0:
                    self.berries.remove(berry)
                    
        UI().delay_print(player.name + " used an Razz Berry on wild " + pokemon.name)
        UI().delay_print("The wild " + pokemon.name + "'s catch rate has increased!")       
        return pokemon   

    # # Nanab Berry
    # def nanab_berry(self, player, pokemon: Pokemon, check: bool):
    #     if pokemon.master != None:
    #         UI().delay_print("Would have no effect")
    #         return -1

    #     if check:
    #         return 0
        
    #     Makes wild Pokémon move less when trying to capture them
        
    #     for berry in self.berries:
    #         if berry[NAME] == "Nanab Berry":
    #             berry[QUANTITY] -= 1
    #             if berry[QUANTITY] == 0:
    #                 self.berries.remove(berry)
                    
    #     UI().delay_print(player.name + " used an Nanab Berry on wild " + pokemon.name)
    #     UI().delay_print("The wild " + pokemon.name + "'s movement has decreased!")       
    #     return pokemon      
    
    # Wepear Berry
    # Bluk_Berry
    
    # Pomeg Berry
    # Kelpsy Berry
    # Qualot Berry
    # Hondew Berry
    # Grepa Berry
    # Tomato Berry
    # Cornn Berry
    # Magost Berry
    # Rabuta Berry
    # Nomel Berry
    # Spelon Berry
    # Pamtre Berry
    # Watmel Berry
    # Durin Berry
    # Belue Berry
    
    #FALTAN POR CONFIGURAR EN BATALLA
    # Pinap Berry
    # Liechi Berry
    # Ganlon Berry
    # Salac Berry
    # Petaya Berry
    # Apricot Berry
    # Lansat Berry
    # Starf Berry
    # Enigma Berry
    # Micle Berry
    # Custap Berry
    # Jabocca Berry
    # Rowap Berry
    