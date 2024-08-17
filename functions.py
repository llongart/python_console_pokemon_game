from random import choice, randint
from os import system
from json import *
from constants import *
from Models.player import *
from Models.pokemon import *
from Models.attack import *
from Models.battle import *
from Models.command import *
from Models.turn import *
from Models.item import *
from Models.ui import *
from Models.bag import *
from math import *
from keyboard import *

# https://www.youtube.com/watch?v=_6KKQvScwjA 


def get_db_pokemon():
    # Get all pokemons with types and base stats
    try:
        with open(path_pokedex, 'r') as pokedex:
            content = pokedex.read()
            db_pokemon_list = loads(content)     
    except Exception:
            db_pokemon_list  = None 

    return db_pokemon_list

def get_db_base_exp_ev():
    # Get Base Exp and EVs yield by pokemon name
    try:    
        with open(path_base_ev, 'r') as baseExp_EV:
            content = baseExp_EV.read()
            db_base_ev_list = loads(content)      
    except Exception:
            db_base_ev_list  = None 
    return db_base_ev_list

def get_db_attacks():
    # Get the moves list
    try:
        with open(path_attacks, 'r') as attacks:
            content = attacks.read()
            db_attack_list = loads(content) 
    except Exception:
            db_attack_list = None 
    return db_attack_list

def get_db_abilities():
    # Get abilities
    try:
        with open(path_abilities, 'r') as abilities:
            content = abilities.read()
            db_abilities = loads(content)        
    except Exception:
            db_abilities = None    

    return db_abilities

def get_db_learnsets():
    # Get learnsets
    try:
        with open(path_learnsets, 'r') as learnsets:
            content = learnsets.read()
            db_learnsets = loads(content)        
    except Exception:
            db_learnsets = None
    return db_learnsets    

def get_db_savegame():
    # Get savegame
    try:
        with open(path_savegame, 'r') as savegame:
            content = savegame.read()
            db_savegame = loads(content)        
    except Exception:
            db_savegame = None
    return db_savegame
    
def get_database():
    global db_pokemon_list, db_base_ev_list, db_attack_list, db_abilities, db_learnsets, db_savegame

    db_pokemon_list = get_db_pokemon()
    db_base_ev_list = get_db_base_exp_ev()
    db_attack_list = get_db_attacks()
    db_abilities = get_db_abilities()
    db_learnsets = get_db_learnsets()
    db_savegame = get_db_savegame()

# Player/Rival data from savedata
#   object = PLAYER or object = RIVAL
def get_trainer_data_from_savegame(player_obj):
    player = Player(db_savegame[player_obj][GENDER], db_savegame[player_obj][NAME])
    player.badges = db_savegame[player_obj][BADGES]
    
    # Bag
    player.bag.items = db_savegame[player_obj][BAG][ITEMS]
    player.bag.medicine = db_savegame[player_obj][BAG][MEDICINE]
    player.bag.tm_hm = db_savegame[player_obj][BAG][TM_HM]
    player.bag.berries = db_savegame[player_obj][BAG][BERRIES]
    player.bag.key_items = db_savegame[player_obj][BAG][KEY_ITEMS]
    player.bag.free_space = db_savegame[player_obj][BAG][FREE_SPACE]

    i = 0
    for pokemon in db_savegame[player_obj][POKEMONS]:
        player_pokemon = Pokemon(pokemon[NAME], pokemon[LEVEL], pokemon[TYPE1], pokemon[TYPE2])
        
        player_pokemon.current_status = pokemon[CURRENT_STATUS]
        j = 0
        for attack in pokemon[ATTACKS]:
            pokemon_attack = db_attack_list[attack[0]]
            player_pokemon.attacks.insert(j, 
                Attack(
                    pokemon_attack[NAME], 
                    pokemon_attack[TYPE], 
                    pokemon_attack[CATEGORY], 
                    int(pokemon_attack[POWER]), 
                    int(pokemon_attack[ACCURACY]), 
                    int(attack[2]), # PP
                    attack[1] # STAGE
                )
            ) 
            j += 1

        player_pokemon.stats = pokemon[STATS]
        player_pokemon.current_hp = player_pokemon.stats[HP] #pokemon[CURRENT_HP]
        player_pokemon.base_stats = pokemon[BASE_STATS]
        player_pokemon.iv = pokemon[IV]
        player_pokemon.ev = pokemon[EV]        
        player_pokemon.nature_type = pokemon[NATURE_TYPE]
        player_pokemon.nature = pokemon[NATURE_VAL]
        player_pokemon.ability = pokemon[ABILITY]
        player_pokemon.base_exp = pokemon[BASE_EXP]
        player_pokemon.growning_type = pokemon[GROWNING_TYPE_VAL]
        player_pokemon.current_exp = pokemon[CURRENT_EXP]
        player_pokemon.exp_next_level = pokemon[EXP_NEXT_LEVEL]       
        player_pokemon.learnset = db_learnsets[str(player_pokemon.name).upper()] 
        player_pokemon.compute_stats()
        player_pokemon.master = pokemon[MASTER]
        player_pokemon.held = pokemon[HELD]
        player_pokemon.friendship = pokemon[FRIENDSHIP]
        player_pokemon.catch_rate = pokemon[CATCH_RATE]
        player.pokemons.insert(i, player_pokemon)
        
        i += 1
        
    player.money = db_savegame[player_obj][MONEY]    

    return player

def data_to_savegame(player: Player):
    # Get data from Player/Rival
    gender = player.gender
    name = player.name

    pokemons = []
    i = 0
    for pokemon in player.pokemons:
        attacks = []
        j = 0
        for attack in player.pokemons[i].attacks:
            attacks.insert(j, [attack.name, attack.stage, attack.pp])
            j += 1   

        pokemons.insert(i, 
            { 
                NAME: pokemon.name, 
                LEVEL: pokemon.level, 
                TYPE1: pokemon.type1, 
                TYPE2: pokemon.type2, 
                CURRENT_HP: pokemon.current_hp, 
                CURRENT_STATUS: pokemon.current_status, 
                ATTACKS: attacks,
                STATS: pokemon.stats, 
                BASE_STATS: pokemon.base_stats, 
                IV: pokemon.iv, 
                EV: pokemon.ev,
                NATURE_TYPE: pokemon.nature_type, 
                NATURE_VAL: pokemon.nature, 
                ABILITY: pokemon.ability, 
                BASE_EXP: pokemon.base_exp, 
                GROWNING_TYPE_VAL: pokemon.growning_type, 
                CURRENT_EXP: pokemon.current_exp, 
                EXP_NEXT_LEVEL: pokemon.exp_next_level, 
                EVOLUTION: pokemon.evolution,
                MASTER: pokemon.master,
                HELD: pokemon.held,
                FRIENDSHIP: pokemon.friendship,
                CATCH_RATE: pokemon.catch_rate
            }         
        )  
        i += 1 

    bag = {
        ITEMS: player.bag.items, 
        MEDICINE: player.bag.medicine, 
        TM_HM: player.bag.tm_hm, 
        BERRIES: player.bag.berries, 
        KEY_ITEMS: player.bag.key_items, 
        FREE_SPACE: player.bag.free_space
    }
    money = player.money
    badges_list = { 
        BADGE1: player.badges[BADGE1],
        BADGE2: player.badges[BADGE2],
        BADGE3: player.badges[BADGE3],
        BADGE4: player.badges[BADGE4],
        BADGE5: player.badges[BADGE5],
        BADGE6: player.badges[BADGE6],
        BADGE7: player.badges[BADGE7],
        BADGE8: player.badges[BADGE8]
    }

    return { NAME: name, GENDER: gender, MONEY: money, BADGES: badges_list, POKEMONS: pokemons, BAG: bag }

def initialize_trainer_data(gender: int, nickname: str, pokemon_chosen: str):
    player = Player(gender, nickname)
    
    pokemon = db_pokemon_list[pokemon_chosen]
    # Check if the pokemon chosen have more than one type
    if len(pokemon) > 8:
        pokemon1 = Pokemon(pokemon[NAME], 5, pokemon[TYPE1], pokemon[TYPE2])
    else:
        pokemon1 = Pokemon(pokemon[NAME], 5, pokemon[TYPE1], None)

    pokemon1.base_stats = {
        HP: pokemon[HP],
        ATTACK: pokemon[ATTACK],
        DEFENSE: pokemon[DEFENSE],
        SPATTACK: pokemon[SPATTACK],
        SPDEFENSE: pokemon[SPDEFENSE],
        SPEED: pokemon[SPEED]
    }
    
    pokemon1.iv = {
        HP: randint(0, 31),
        ATTACK: randint(0, 31),
        DEFENSE: randint(0, 31),
        SPATTACK: randint(0, 31),
        SPDEFENSE: randint(0, 31),
        SPEED: randint(0, 31)
    }

    pokemon1.ev = { #https://www.cpokemon.com/effort_value_points.php
        HP: db_base_ev_list[pokemon[NAME]][HP_YIELD],
        ATTACK: db_base_ev_list[pokemon[NAME]][ATTACK_YIELD],
        DEFENSE: db_base_ev_list[pokemon[NAME]][DEFENSE_YIELD],
        SPATTACK: db_base_ev_list[pokemon[NAME]][SPATTACK_YIELD],
        SPDEFENSE: db_base_ev_list[pokemon[NAME]][SPDEFENSE_YIELD],
        SPEED: db_base_ev_list[pokemon[NAME]][SPEED_YIELD]
    }

    if (pokemon1.name == "Bulbasaur"):
        attack1 = db_attack_list["TACKLE"]
        attack2 = db_attack_list["GROWL"]
    elif (pokemon1.name == "Charmander"):
        attack1 = db_attack_list["SCRATCH"]
        attack2 = db_attack_list["GROWL"]
    elif (pokemon1.name == "Squirtle"):
        attack1 = db_attack_list["TACKLE"]
        attack2 = db_attack_list["TAIL WHIP"]  

    pokemon1.attacks = [
        Attack(attack1[NAME], attack1[TYPE], attack1[CATEGORY], int(attack1[POWER]), int(attack1[ACCURACY]), int(attack1[PP]), STAGE_0),
        Attack(attack2[NAME], attack1[TYPE], attack2[CATEGORY], int(attack2[POWER]), int(attack2[ACCURACY]), int(attack2[PP]), STAGE_0),
    ]

    pokemon1.ability = {
        FIRST: db_abilities[pokemon1.name][FIRST],
        SECOND: db_abilities[pokemon1.name][SECOND],
        HIDDEN: db_abilities[pokemon1.name][HIDDEN]
    }

    nature_list = list(NATURE.items())
    random_nature = randint(0, len(NATURE) - 1)
    nature_selected = nature_list[random_nature][0]
    pokemon1.nature_type = nature_selected
    pokemon1.nature = NATURE[nature_selected]

    pokemon1.compute_stats()

    pokemon1.base_exp = db_base_ev_list[pokemon[NAME]][BASE_EXP]
    pokemon1.current_status = ST_NORMAL
    pokemon1.current_hp = pokemon1.stats[HP]

    growning_type_list = list(GROWNING_TYPE.items())
    random_growning_type = randint(0, len(GROWNING_TYPE) - 1)
    growning_type_selected = growning_type_list[random_growning_type]

    pokemon1.growning_type = growning_type_selected[1]
    pokemon1.get_growning_type_exp()

    pokemon1.current_exp = 0  
    
    pokemon1.learnset = db_learnsets[str(pokemon1.name).upper()]
    pokemon1.master = 1
    pokemon1.catch_rate = 0

    player.pokemons = [pokemon1]

    potion = Item("Potion", MEDICINE)
    #potion.id = "001"
    potion.sellable = True
    potion.use = 0 # From bag
    potion.effect = 20
    
    super_potion = Item("Super Potion", MEDICINE)
    #super_potion.id = "002"
    super_potion.sellable = True
    super_potion.use = 0 # From bag
    super_potion.effect = 60

    player.bag.medicine.insert(0, { NAME : potion.name, 'QUANTITY': 3 })
    player.bag.medicine.insert(1, { NAME : super_potion.name, 'QUANTITY': 1 })
    
    return player

def initialize_game():

    if db_savegame == None: # No savegame found
        system("cls")
        
        gender = None
        # Player
        print("Are you a boy or a girl? ")
        print("1. Boy      2. Girl")
        while gender not in ['1', '2']:
            gender = input()

        system("cls")
        
        nickname = input("Please tell me your name: ")
        
        system("cls")
        print("Nice to meet you "+nickname+'\n')

        # Rival introduce
        print("This is your rival, Rain Mustard")
        print("He's one of the must hardest pokemon trainer around Forktown")
        print("Now, you can choose one of three pokemons to begin your journey\n")
        
        # Choose a pokemon to start
        while True:
            print("Please choose one pokeball")
            print("1. Pokeball #1       2. Pokeball #2      3.Pokeball #3")
        
            pokeball = None
            while pokeball not in ['1', '2', '3']:
                pokeball = input()
            
            if pokeball == '1':
                print("Do you want to start with Bulbasaur?")
                pokemon_chosen = "Bulbasaur"
                pokemon_rival = "Charmander"
            if pokeball == '2':
                print("Do you want to start with Charmander?")
                pokemon_chosen = "Charmander"
                pokemon_rival = 'Squirtle'
            if pokeball == '3':
                print("Do you want to start with Squirtle?")
                pokemon_chosen = "Squirtle"
                pokemon_rival = "Bulbasaur"

            print("Yes       No")

            answer = None
            while str(answer).upper() not in ['YES', 'Y', 'NO', 'N']:
                answer = input()
            
            if str(answer).upper() in ['YES', 'Y']:
                break
            else:
                system("cls")
        
        # Initializing new game Player
        player = initialize_trainer_data(gender, nickname, pokemon_chosen)

        # Initializing new game Rival
        rival = initialize_trainer_data(1, "Rain Mustard", pokemon_rival)

    else: # Savegame found it

        # player data from savedata
        player = get_trainer_data_from_savegame(PLAYER)
        # Rival data from savedata
        rival = get_trainer_data_from_savegame(RIVAL)

    return Battle(player, rival, WEATHER_TYPE[0])

def select_attack(pokemon: Pokemon):
    global db_attack_list
    
    i = 0
    atk = ''
    no_pp = 0
    for attack in pokemon.attacks:
            if attack.pp == 0:
                no_pp += 1    
    
    if no_pp != len(pokemon.attacks):        
        for attack in pokemon.attacks:               
            if i == 0:
                
                atk = "ATTACK (Q): "+ attack.name + " " + str(attack.pp)+"/"+str(db_attack_list[attack.name][PP])
                if len(pokemon.attacks) == 1:
                    print(atk) 
            if i == 1:
                atk = atk + "       ATTACK (W): "+attack.name + " " + str(attack.pp)+"/"+str(db_attack_list[attack.name][PP])
                print(atk)
            if i == 2:
                atk = ''
                atk = "ATTACK (E): "+attack.name + " " + str(attack.pp)+"/"+str(db_attack_list[attack.name][PP]) + "       " + atk
                if len(pokemon.attacks) == 3:
                    print(atk)
            if i == 3:
                atk = atk + "ATTACK (R): "+attack.name + " " + str(attack.pp)+"/"+str(db_attack_list[attack.name][PP])
                print(atk)
            
            i += 1

        print("Or press ESC to back...")
        print("------------------------------")        
        command = None

        while not command:
            try:
                if is_pressed('Q') and len(pokemon.attacks) >= 1:
                    if pokemon.attacks[0].pp > 0:
                        command = Command({ ATTACK : 0})
                        pokemon.attacks[0].pp -= 1
                    else:
                        UI().delay_print("This move has no more pp!")                    
                    break
                    
                if is_pressed('W') and len(pokemon.attacks) >= 2:
                    if pokemon.attacks[1].pp > 0:
                        command = Command({ ATTACK : 1}) 
                        pokemon.attacks[1].pp -= 1                       
                    else:
                        UI().delay_print("This move has no more pp!")                        
                    break
                        
                if is_pressed('E') and len(pokemon.attacks) >= 3:
                    if pokemon.attacks[2].pp > 0:
                        command = Command({ ATTACK : 2}) 
                        pokemon.attacks[2].pp -= 1   
                    else:
                        UI().delay_print("This move has no more pp!")
                    break    
                if is_pressed('R') and len(pokemon.attacks) == 4:
                    if pokemon.attacks[3].pp > 0:
                        command = Command({ ATTACK : 3}) 
                        pokemon.attacks[3].pp -= 1   
                    else:
                        UI().delay_print("This move has no more pp!")
                    break
                if is_pressed('ESC'):
                    break                     
            except Exception:
                pass  
    else:
        command = Command({ ATTACK : -1}) # No more moves (PP) so use STRUGGLE
    
    return command

def change_pokemon(player: Player, index: int):
    if player.pokemons[index].in_use:
        UI().delay_print("This pokemon is currently in battle!")
        return None
        
    return Command({ POKEMON : index})  

def select_pokemon(player: Player, pokemon: Pokemon):
    i = 1                
    for pokemon_bag in player.pokemons:
        print(str(i)+ ". "+pokemon_bag.name)
        i += 1
    
    command = None
    while True:
        try:
            if is_pressed('Q') and len(player.pokemons) > 0:
                command = change_pokemon(player, 0)
                break 
            if is_pressed('W') and len(player.pokemons) > 1:
                command = change_pokemon(player, 1) 
                break 
            if is_pressed('E') and len(player.pokemons) > 2:
                command = change_pokemon(player, 2)
                break 
            if is_pressed('R') and len(player.pokemons) > 3:
                command = change_pokemon(player, pokemon, 3)
                break 
            if is_pressed('T') and len(player.pokemons) > 4:
                command = change_pokemon(player, pokemon, 4) 
                break 
            if is_pressed('Y') and len(player.pokemons) > 5:
                command = change_pokemon(player, pokemon, 5)
                break 
            if is_pressed('ESC'):
                break                                                                                                               
        except Exception:
            pass 

    return command

def get_bag(item_type: str, bag: Bag):
    return {
        ITEMS: bag.items,
        MEDICINE: bag.medicine,
        TM_HM: bag.tm_hm,
        BERRIES: bag.berries,
        KEY_ITEMS: bag.key_items,
        FREE_SPACE: bag.free_space
    }.get(item_type, None)

def get_bag_command(player: Player, bag_object: str, pokemon1: Pokemon, pokemon2: Pokemon):
    
    player_bag = get_bag(bag_object, player.bag)

    i = 1
    for item in player_bag:
        print(str(i) + ". " + item[NAME] + " x "+ str(item['QUANTITY']))
        i += 1
    
    if len(player_bag) > 0:
        print("Or type 'Q' or 'ESC' to exit...")
        
        answer = None
        while answer not in range(1, i):
            answer = input("Select item: ")
            if not answer.isnumeric():
                if str(answer).upper() in ['Q', 'ESC']:
                    break
                else:
                    answer = None
            else:
                index = int(answer) - 1 

                # Call function from item selected with Check = True 
                # just to verify if the item can be consumed
                name = str(player_bag[index][NAME]).lower().replace(' ', '_')
                function_name = getattr(player.bag, name)

                # return -1 if message is "Would have take no effect"
                # return None if item selected is in (Ether, Max Ether) 
                # and Q or ESC is typed to go back to item selection
                # if name not in ('razz_berry'):
                if function_name(player, pokemon1, True) not in (None, -1):
                    return Command({ BAG : player_bag[index]})
                else:
                    answer = None
                # else:
                #     if function_name(player, pokemon2, True) not in (None, -1):
                #         return Command({ BAG : player_bag[index]})
                #     else:
                #         answer = None
    else:
        print("No items here!")

    return None 

def use_item_from_bag(player, pokemon1, pokemon2):
    print("Q. Items     W. Medicine")#     E. TH/HM")
    print("A. Berries   S. Key Items")#    D. Free space")
    print("Or press ESC to back...")
    print("------------------------------")
    
    command = None
    while True:
        try:
            if is_pressed('Q'):
                command = get_bag_command(player, ITEMS, pokemon1, pokemon2)
                break
            if is_pressed('W'):
                command = get_bag_command(player, MEDICINE, pokemon1, pokemon2)
                break
            # if is_pressed('E'):
            #     command = get_bag_command(player, TM_HM)
            #     break
            if is_pressed('A'):
                command = get_bag_command(player, BERRIES, pokemon1, pokemon2)
                break     
            if is_pressed('S'):
                command = get_bag_command(player, KEY_ITEMS, pokemon1, pokemon2)
                break
            # if is_pressed('D'):
            #     command = get_bag_command(player, FREE_SPACE)
            #     break   
            if is_pressed('ESC'):
                break                                                                                           
        except Exception:
            pass

    return command

def ask_command(battle: Battle): #player: Player, pokemon: Pokemon
    command = None
    
    player = battle.player1
    pokemon = battle.pokemon1
    
    while not command:

        print("------------------------------")
        print(player.name + ", what will "  +pokemon.name + " do? ")
        print("1: ATTACK        2: POKEMON")
        print("3: BAG           4: FLEE")
        print("------------------------------")

        while not command:
            try:                                 
                if is_pressed('1'): # Attack
                    command = select_attack(pokemon)
                    break 
                
                if is_pressed('2'): # Change pokemon
                    command = select_pokemon(player, pokemon)
                    break

                if is_pressed('3'): # Use item from bag
                    command = use_item_from_bag(player, pokemon, battle.pokemon2)
                    break

                if is_pressed('4'): # Flee from battle
                    command = Command({ FLEE : None}) 
                    break 
                    
            except Exception:
                pass     
    
    return command  

def check_cpu_pokemon_effectiveness(cpu: Player, player_pokemon: Pokemon):
    # Check effectiveness CPU_POKEMON vs PLAYER_POKEMON
    index = 0
    for pokemon in cpu.pokemons:
        effectiveness = DEFENSE_EFFECTIVENESS[pokemon.type1][player_pokemon.type1] # USE type2 too
        if effectiveness not in (W, N):
            # Look for another pokemon
            index += 1
        else:
            # Keep this pokemon
            break        
    
    # If pokemon it's different from first pokemon then change
    # If index = 6 then cpu wont change because none pokemon have advantage over PLAYER_POKEMON 
    # If index = 0 first pokemon have advantage over PLAYER_POKEMON
    if index not in (0, 6) and not cpu.pokemons[index].in_use:
        return index

    return None

def check_cpu_current_hp(cpu_pokemon: Pokemon):
    global max_curation_usage

    hp_percentage = int(cpu_pokemon.stats[HP] * 25 / 100) # 25% HP = use curation
    if cpu_pokemon.current_hp <= hp_percentage and max_curation_usage < 3: # Max 3 potions in battle
        max_curation_usage += 1
        return True

    return False  

def select_cpu_move_to_use(cpu_pokemon: Pokemon, player_pokemon: Pokemon):
    global sta_count

   # Attack Selection   
    attack_moves = {}
    status_moves = {}
    iterations = 0
    while iterations < len(cpu_pokemon.attacks):
        if cpu_pokemon.attacks[iterations].power > 0:
            attack_moves[cpu_pokemon.attacks[iterations].name] = [ cpu_pokemon.attacks[iterations].power, cpu_pokemon.attacks[iterations].ztype, iterations ] 
        else:
            status_moves[cpu_pokemon.attacks[iterations].name] = [ cpu_pokemon.attacks[iterations].power, cpu_pokemon.attacks[iterations].ztype, iterations ] 
        iterations += 1
    
    sorted_atk_moves = sorted(attack_moves.items(), key=lambda x: x[1], reverse=True)
    sorted_sta_moves = sorted(status_moves.items(), key=lambda x: x[1], reverse=True)
    
    effec_atk = {}
    if len(sorted_atk_moves) > 0:
        atk_move1 = sorted_atk_moves[0][1][2]    
        move_type = sorted_atk_moves[0][1][1]
        effec_atk[atk_move1] = DEFENSE_EFFECTIVENESS[move_type][player_pokemon.type1] # USE type2 too
    if len(sorted_atk_moves) > 1:
        atk_move2 = sorted_atk_moves[1][1][2]
        move_type = sorted_atk_moves[1][1][1]
        effec_atk[atk_move2] = DEFENSE_EFFECTIVENESS[move_type][player_pokemon.type1] # USE type2 too 
    if len(sorted_atk_moves) > 2:
        atk_move3 = sorted_atk_moves[2][1][2]
        move_type = sorted_atk_moves[2][1][1]
        effec_atk[atk_move3] = DEFENSE_EFFECTIVENESS[move_type][player_pokemon.type1] # USE type2 too 
    if len(sorted_atk_moves) > 3:
        atk_move4 = sorted_atk_moves[3][1][2]
        move_type = sorted_atk_moves[3][1][1]      
        effec_atk[atk_move4] = DEFENSE_EFFECTIVENESS[move_type][player_pokemon.type1] # USE type2 too  
    
    effec_sta = {}
    sta_move1 = sta_move2 = sta_move3 = sta_move4 = None # None for verification on sta_count
    if len(sorted_sta_moves) > 0:
        sta_move1 = sorted_sta_moves[0][1][2]
        move_type = sorted_sta_moves[0][1][1]
        effec_sta[sta_move1] = DEFENSE_EFFECTIVENESS[move_type][player_pokemon.type1] # USE type2 too        
    if len(sorted_sta_moves) > 1:
        sta_move2 = sorted_sta_moves[1][1][2]
        move_type = sorted_sta_moves[1][1][1]
        effec_sta[sta_move2] = DEFENSE_EFFECTIVENESS[move_type][player_pokemon.type1] # USE type2 too           
    if len(sorted_sta_moves) > 2:
        sta_move3 = sorted_sta_moves[2][1][2]
        move_type = sorted_sta_moves[2][1][1]
        effec_sta[sta_move3] = DEFENSE_EFFECTIVENESS[move_type][player_pokemon.type1] # USE type2 too           
    if len(sorted_sta_moves) > 3:
        sta_move4 = sorted_sta_moves[3][1][2]
        move_type = sorted_sta_moves[3][1][1]
        effec_sta[sta_move4] = DEFENSE_EFFECTIVENESS[move_type][player_pokemon.type1] # USE type2 too           
    
    sorted_effec_atk = sorted(effec_atk.items(), key=lambda x: x[1], reverse=False)
    sorted_effec_sta = sorted(effec_sta.items(), key=lambda x: x[1], reverse=False)
    
    moves_array = []
    # PP atk move 
    for move in sorted_effec_atk:
        if cpu_pokemon.attacks[move[0]].pp > 0:
            moves_array.insert(0, move[0])
            break

    # PP sta move
    if sta_count < 5: # Can't use a STATUS move more than 5 times in a battle
        for move in sorted_effec_sta:
            if cpu_pokemon.attacks[move[0]].pp > 0:
                moves_array.insert(1, move[0])
                break        
    
    if len(moves_array) == 0:
        return -1
    
    move_to_use = choice(moves_array)
    if move_to_use in [sta_move1, sta_move2, sta_move3, sta_move4]:
        sta_count += 1
    
    return move_to_use

def cpu_command(cpu, cpu_pokemon: Pokemon, player: Player, player_pokemon: Pokemon):
    
    # Check if have to change pokemon
    index = check_cpu_pokemon_effectiveness(cpu, player_pokemon)
    if index != None:
        return Command({ POKEMON: index })

    # Check current HP
    if check_cpu_current_hp(cpu_pokemon):
        return Command({ BAG: {NAME: 'Potion', QUANTITY: 1}})

    # Select move to use
    return Command({ ATTACK: select_cpu_move_to_use(cpu_pokemon, player_pokemon) })

def startbattle(battle: Battle):
    system("cls")
    print("\n")
    print("------------------------------")
    print("|       POKEMON BATTLE       |")
    print("------------------------------")
    print(" ", battle.pokemon1.name, "vs", battle.pokemon2.name)
    
    battle.pokemon1.in_use = battle.pokemon2.in_use = True
    
    while not battle.is_finished():
        
        print("Weather: " + battle.weather + "\n")
        
        # Command
        command1 = ask_command(battle) #battle.player1, battle.pokemon1, 
        # Check if pokemon 1 wants to flee
        if command1 != None and battle.check_flee(command1, battle.pokemon1): 
            break

        # Check if pokemon 2 wants to flee
        command2 = cpu_command(battle.player2, battle.pokemon2, battle.player1, battle.pokemon1)
        if command2 != None and battle.check_flee(command2, battle.pokemon2): 
            break

        turn = Turn()
        turn.command1 = command1
        turn.command2 = command2

        if turn.can_start():
            battle.execute_turn(turn)
            battle.print_current_status() 
        
def savegame(player: Player, rival: Player):
    # Save the game on .json
    db_savegame = {}

    # Get data from Player from actual game
    db_savegame[PLAYER] = data_to_savegame(player)
    
    # Get data from Rival from actual game
    db_savegame[RIVAL] = data_to_savegame(rival) 

    # Save the current game
    try:
        with open(path_savegame, 'w') as savegame:
            dump(db_savegame, savegame, indent = 4)      
    except Exception:
            print("Error al intentar guardar la partida!")
