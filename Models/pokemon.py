from constants import *
from Models.attack import *
from Models.ui import *
from json import *

class Pokemon:

    def __init__(self, name, level, type1, type2):
        self.name = name
        self.level = level
        self.type1 = type1
        self.type2 = type2
        self.current_hp = 0
        self.current_status = ST_NORMAL
        self.attacks = []
        self.stats = {}
        self.base_stats = {}
        self.iv = {}
        self.ev = {}
        self.nature_type = None
        self.nature = {}
        self.def_effectiveness = {}
        self.ability = {}
        self.base_exp = 0
        self.growning_type = None
        self.current_exp = 0
        self.exp_next_level = 0
        self.evolution = self.get_evolution()
        self.in_use = False
        self.learnset = None
        # master = 1 if the winning Pokémon's current owner is its Original Trainer
        #          1.5 if the Pokémon was gained in a domestic trade
        #          1.7 if the Pokémon was gained in an international trade (in Generation V+, this is instead approximated very closely as 6963/4096)        
        self.master = None
        self.held = None
        self.semi_inv_turn = None
        self.last_move = None
        self.cant_be_affected_by = []
        self.last_berry_used = None
        self.affected_by = None
        self.friendship = 0
        self.catch_rate = 10 # https://bulbapedia.bulbagarden.net/wiki/Catch_rate
                             # https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_catch_rate
        self.stats_stages = {
            HP: 0,
            ATTACK: 0,
            DEFENSE: 0,
            SPATTACK: 0,
            SPDEFENSE: 0,
            SPEED: 0,
            ACCURACY: 0,
            EVASION: 0
        }

        # In case level not between 1 and 100
        if self.level < 1:
            self.level = 1
        elif self.level > 100:
            self.level = 100
    
    # Get hp stat
    def compute_hp_stat(self):
        formula = (2 * self.base_stats[HP] + self.iv[HP] + (self.ev[HP] / 4))
        formula = formula * self.level / 100
        return int(formula + self.level + 10)

    # Get individual stats
    def compute_individual_stat(self, stat):
        formula = (2 * self.base_stats[stat] + self.iv[stat] + (self.ev[stat] / 4))
        formula = ( formula * self.level / 100 ) + 5
        return int(formula * self.nature[stat])
    
    # Assign stats to the pokemon
    def compute_stats(self):
        self.stats = {
            HP: self.compute_hp_stat(),
            ATTACK: self.compute_individual_stat(ATTACK),
            DEFENSE: self.compute_individual_stat(DEFENSE),
            SPATTACK: self.compute_individual_stat(SPATTACK),
            SPDEFENSE: self.compute_individual_stat(SPDEFENSE),
            SPEED: self.compute_individual_stat(SPEED)
        }
    
    # Get exp formula from growning type
    def get_growning_type_exp(self):
        n = self.level

        if self.growning_type == ERRATIC:
            if n < 50: # Level is less than 50
                self.exp_next_level = int(((pow(n, 3) * (100 - n)) / 50))
            elif 50 <= n < 68: # Level is greater or equal to 50 and less than 68
                self.exp_next_level = int((pow(n, 3) * (150 - n)) / 100)
            elif 68 <= n < 98: # Level is greater or equal to 68 and less than 98
                self.exp_next_level = int((pow(n, 3) * ((1911 - 10 * n) / 3)) / 500)
            elif n >= 98: # Level is between 98 and 100
                self.exp_next_level = int((pow(n, 3) * (160 - n)) / 100)
            return

        if self.growning_type == FAST:
            self.exp_next_level = int((4 * pow(n, 3)) / 5)
            return

        if self.growning_type == MEDIUM_FAST:
            self.exp_next_level = int(pow(n, 3))
            return

        if self.growning_type == MEDIUM_SLOW:
            self.exp_next_level = int(((6/5) * pow(n, 3)) - (15 * pow(n, 2)) + (100 * n) - 140)
            return

        if self.growning_type == SLOW:
            self.exp_next_level = int((5 * pow(n, 3)) / 4)
            return

        if self.growning_type == FLUCTUATING:
            if n < 15: # Level is less than 15
                self.exp_next_level = int(pow(n, 3) * (((((n + 1) / 3)) + 24) / 50))
            elif 15 <= n < 36: # Level is greater or equal to 15 and less than 36
                self.exp_next_level = int(pow(n, 3) * ((n + 14) / 50 ))
            elif n >= 36: # Level is between 36 and 100
                self.exp_next_level = int(pow(n, 3) * (((n / 2) + 32) / 50))

    # Get evolution of current pokemon
    def get_evolution(self):        
        # Get evolution list
        try:
            with open(path_evolutions, 'r') as pokedex:
                content = pokedex.read()
                db_evolutions = loads(content)     
        except Exception:
                db_evolutions  = None         

        return db_evolutions[self.name]

    # Check if pokemon can evolve
    def check_evolution(self, pokemon):
        global is_evolving

        is_evolving = False 
        if str(pokemon.evolution['CONDITION']).isnumeric():
            if pokemon.level >= int(pokemon.evolution['CONDITION']):
                is_evolving = True
            
        return is_evolving   

    # Do pokemon evolution and return the new pokemon with its stats computed, attacks, etc.
    def do_evolution(self, pokemon):
        global db_pokemon_list, db_base_ev_list, db_attack_list

        # Get all pokemons with types and base stats
        try:
            with open(path_pokedex, 'r') as pokedex:
                content = pokedex.read()
                db_pokemon_list = loads(content)     
        except Exception:
                db_pokemon_list  = None 

        # Get Base Exp and EVs yield by pokemon name
        try:    
            with open(path_base_ev, 'r') as baseExp_EV:
                content = baseExp_EV.read()
                db_base_ev_list = loads(content)      
        except Exception:
                db_base_ev_list  = None 

        # Get the moves list
        try:
            with open(path_attacks, 'r') as attacks:
                content = attacks.read()
                db_attack_list = loads(content) 
        except Exception:
                db_attack_list = None 

        name = pokemon.name
        level = pokemon.level
        current_exp = pokemon.current_exp
        current_hp = pokemon.current_hp

        pokevolution = db_pokemon_list[pokemon.evolution['EVOLUTION']]
        # Check if the pokemon chosen have more than one type
        if len(pokevolution) > 8:
            evolution = Pokemon(pokevolution[NAME], level, pokevolution[TYPE1], pokevolution[TYPE2])
        else:
            evolution = Pokemon(pokevolution[NAME], level, pokevolution[TYPE1], None)

        evolution.base_stats = {
            HP: pokevolution[HP],
            ATTACK: pokevolution[ATTACK],
            DEFENSE: pokevolution[DEFENSE],
            SPATTACK: pokevolution[SPATTACK],
            SPDEFENSE: pokevolution[SPDEFENSE],
            SPEED: pokevolution[SPEED]
        }
        
        evolution.iv = {
            HP: pokemon.iv[HP],
            ATTACK: pokemon.iv[ATTACK],
            DEFENSE: pokemon.iv[DEFENSE],
            SPATTACK: pokemon.iv[SPATTACK],
            SPDEFENSE: pokemon.iv[SPDEFENSE],
            SPEED: pokemon.iv[SPEED]   
        }

        evolution.ev = { # https://www.cpokemon.com/effort_value_points.php
            HP: db_base_ev_list[pokevolution[NAME]][HP_YIELD],
            ATTACK: db_base_ev_list[pokevolution[NAME]][ATTACK_YIELD],
            DEFENSE: db_base_ev_list[pokevolution[NAME]][DEFENSE_YIELD],
            SPATTACK: db_base_ev_list[pokevolution[NAME]][SPATTACK_YIELD],
            SPDEFENSE: db_base_ev_list[pokevolution[NAME]][SPDEFENSE_YIELD],
            SPEED: db_base_ev_list[pokevolution[NAME]][SPEED_YIELD]
        }

        
        attack1 = db_attack_list[pokemon.attacks[0].name]
        evolution.attacks.insert(0, Attack(attack1[NAME], attack1[TYPE], attack1[CATEGORY], int(attack1[POWER]), int(attack1[ACCURACY]), int(attack1[PP]), pokemon.attacks[0].stage))
        if len(pokemon.attacks) == 2:
            attack2 = db_attack_list[pokemon.attacks[1].name]
            evolution.attacks.insert(1, Attack(attack2[NAME], attack2[TYPE], attack2[CATEGORY], int(attack2[POWER]), int(attack2[ACCURACY]), int(attack2[PP]), pokemon.attacks[1].stage))
        if len(pokemon.attacks) == 3:
            attack3 = db_attack_list[pokemon.attacks[2].name]
            evolution.attacks.insert(2, Attack(attack3[NAME], attack3[TYPE], attack3[CATEGORY], int(attack3[POWER]), int(attack3[ACCURACY]), int(attack3[PP]), pokemon.attacks[2].stage))
        if len(pokemon.attacks) == 4:
            attack4 = db_attack_list[pokemon.attacks[3].name]
            evolution.attacks.insert(3, Attack(attack4[NAME], attack4[TYPE], attack4[CATEGORY], int(attack4[POWER]), int(attack4[ACCURACY]), int(attack4[PP]), pokemon.attacks[3].stage))

        
        evolution.ability = {
            FIRST: pokemon.ability[FIRST],
            SECOND: pokemon.ability[SECOND],
            HIDDEN: pokemon.ability[HIDDEN]
        }

        evolution.nature_type = pokemon.nature_type
        evolution.nature = pokemon.nature
        evolution.compute_stats()

        evolution.base_exp = db_base_ev_list[pokevolution[NAME]][BASE_EXP]
        evolution.current_status = pokemon.current_status
        evolution.current_hp = current_hp + int(evolution.stats[HP] / 4)
        evolution.growning_type = pokemon.growning_type
        evolution.get_growning_type_exp()
        evolution.current_exp = current_exp
        
        UI().delay_print("Congratulations, your " + name + " has evolved into " + evolution.name)

        return evolution
