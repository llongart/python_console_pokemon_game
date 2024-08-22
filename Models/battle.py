from Models.turn import Turn
from Models.command import Command
from constants import *
from Models.pokemon import *
from Models.player import *
from Models.attack import *
from Models.item import *
from Models.ui import *
from keyboard import *
from time import time
from random import random, randint

class Battle:

    def __init__(self, player1: Player, player2: Player, weather: str):
        self.player1 = player1
        self.player2 = player2
        self.pokemon1 = self.player1.pokemons[0]
        self.pokemon2 = self.player2.pokemons[0]
        self.weather = weather
        self.actual_turn = 0

    # Check if battle has finished
    def is_finished(self):
        finished = self.pokemon1.current_hp <= 0 or self.pokemon2.current_hp <= 0
        if finished:
           self.print_winner()
        return finished
    
    # Check if pokemons wants to flee
    def check_flee(self, command: Command, pokemon: Pokemon):
        if FLEE in command.action.keys():
            UI().delay_print(pokemon.name + " has fleed from battle!\n")
            return True

        return False

    def compute_damage(self, pokemon1: Pokemon, attack: Attack, pokemon2: Pokemon):
        global is_critical_attack, type_effectiveness

        if attack.name == 'NATURAL GIFT':
            if pokemon1.held == None:
                attack.accuracy = 0

            elif pokemon1.held in NATURAL_GIFT:
                    attack.ztype = NATURAL_GIFT[pokemon1.held][TYPE]
                    attack.power = NATURAL_GIFT[pokemon1.held][POWER]
                    pokemon1.last_berry_used = pokemon1.held
                    pokemon1.held = None          
    
        # Get accuracy rate
        if attack.accuracy < 100: 
            rate = int( ( attack.accuracy * 10 ) / 100)
            if ( randint(0, rate) == 0 ):
                return 0

        if attack.category == STATUS:
            return -1       
        
        # Get attack stat from pokemon1 and defense stat from pokemon2 and apply division
        A_D = pokemon1.stats[ATTACK_STAT[attack.category]] / pokemon2.stats[DEFENSE_STAT[attack.category]]
     
        # Number of targets
        targets = 1
        
        weather = 1
        # Weather in battle
        if self.weather in (WEATHER_TYPE[1], WEATHER_TYPE[2]): # Harsh Sunlight/Extremely Harsh Sunlight
            if attack.ztype == 'FIRE':
                weather = 1.5
            elif attack.ztype == 'WATER':
                weather = 0.5
        
        elif self.weather in (WEATHER_TYPE[3], WEATHER_TYPE[4]): # Rain/Heavy Rain
            if attack.ztype == 'FIRE':
                weather = 0.5
            elif attack.ztype == 'WATER':
                weather = 1.5

        # Badge (Only apply another value for generation II, another generation always 1)
        badge = 1

        # Get critical rate per attack stages
        critical = 1
        is_critical_attack = False
        if random() <= attack.stage:
            critical = 1.5
            is_critical_attack = True

        # Get random
        random_val = randint(85, 100) / 100

        # Get STAB 
        stab = 1        
        if pokemon1.type1 == attack.ztype:
            if 'ADAPTABILITY' not in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
                stab = 1.5
            else:
                stab = 2         
            
        # Get Effectiveness
        effectiveness = DEFENSE_EFFECTIVENESS[pokemon2.type1][attack.ztype] 
        if pokemon2.type2 != None:
            effectiveness *= DEFENSE_EFFECTIVENESS[pokemon2.type2][attack.ztype]  

        type_effectiveness = effectiveness

        # Get burn status
        burn = 1
        if pokemon1.current_status == ST_BURNED and 'GUTS' not in (
            pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]
            ) and attack.category == PHYSICAL and attack.name != 'FACADE':
            burn = 0.5
            
        # Other value(Move, Ability, Item)
        other = 1
        
        # self.get_move_value(pokemon1, pokemon2, attack)
        # Move value
        if attack.name in ('STOMP', 'STEAMROLLER') and pokemon2.last_move != None and pokemon2.last_move.name == 'MINIMIZE':
            other *= 2
        elif pokemon2.last_move != None and pokemon2.last_move.name == 'AURORA VEIL' and not is_critical_attack and 'INFILTRATOR' not in (
            pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            other *= 0.5
        elif attack.name in ('EARTHQUAKE', 'MAGNITUDE') and pokemon2.semi_inv_turn == 'DIG':
            other *= 2
        elif pokemon2.last_move != None and pokemon2.last_move.name == 'LIGHT SCREEN' and attack.category == SPECIAL and not is_critical_attack and 'INFILTRATOR' not in (
            pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            other *= 0.5
        elif pokemon2.last_move != None and pokemon2.last_move.name == 'REFLECT' and attack.category == PHYSICAL and not is_critical_attack and 'INFILTRATOR' not in (
            pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            other *= 0.5        
        elif attack.name in ('SURF', 'WHIRLPOOL') and pokemon2.semi_inv_turn == 'DIVE':
            other *= 2
            
        # Ability value
        if 'FLUFFY' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and attack.name in CONTACT_MOVES and attack.ztype != FIRE:
            other *= 0.5
        elif 'FLUFFY' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and attack.name not in CONTACT_MOVES and attack.ztype == FIRE:
            other *= 2           
        elif 'FILTER' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and type_effectiveness > 1:
            other *= 0.75
        elif 'PRISM ARMOR' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and type_effectiveness > 1:
            other *= 0.75
        elif 'SOLID ROCK' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and type_effectiveness > 1:
            other *= 0.75    
        elif 'ICE SCALES' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and attack.category == SPECIAL:
            other *= 0.5
        elif 'MULTISCALE' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and pokemon2.current_hp == pokemon2.stats[HP]:
            other *= 0.5
        elif 'SHADOW SHIELD' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and pokemon2.current_hp == pokemon2.stats[HP]:
            other *= 0.5
        elif 'NEUROFORCE' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and type_effectiveness > 1:
            other *= 1.25   
        elif 'PUNK ROCK' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and attack.name in SOUND_BASED_MOVES:
            other *= 0.5   
        elif 'SNIPER' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and is_critical_attack:
            other *= 1.5  
        elif 'TINTED LENS' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and type_effectiveness < 1:
            other *= 1.25        
                   
        # Item value
        #if pokemon2.held == 'Chilan Berry' and attack.ztype == NORMAL:
            #other *= 0.5
        #el
        # CHILAN BERRY is already on function: damage_multiplier_by_berry_held()
        if pokemon1.held == 'Expert Belt' and type_effectiveness > 1:
            other *= 1.2   
        elif pokemon1.held == 'Life Orb':
            other *= 1.3
        elif pokemon1.held == 'Metronome':
            consecutive_landed_move = 1 # Provisional
            other *= 1 + (0.2 * consecutive_landed_move)
            if other > 2:
                other *= 2
        elif pokemon2.held in DAMAGE_REDUCING_BERRIES and type_effectiveness > 1:
            move_effect = DEFENSE_EFFECTIVENESS[pokemon2.type1][attack.ztype]
            if pokemon2.ztype != None and move_effect != R:
                move_effect = DEFENSE_EFFECTIVENESS[pokemon2.type2][attack.ztype]
                
            if move_effect == R:
                other *= 0.5                                   
                         
        # Modifier
        modifier = targets * weather * badge * critical * random_val * stab * effectiveness * burn * other

        # Return Damage formula
        damage = ( (2 * pokemon1.level) / 5 ) + 2
        damage = damage * attack.power * A_D
        damage = (damage / 50) + 2
        damage = damage * modifier
                    
        return int(damage)  

    def get_item(self, item, player, pokemon):
        # Get the corresponding function name from item in Bag() class
        # example: player.bag.super_potion()
        name = str(item).lower().replace(' ', '_')
        function_name = getattr(player.bag, name)

        # Call the function from function_name with arguments
        # example: player.bag.super_potion(argument1, argument2)

        if name not in ('razz_berry'):
            return function_name(player, pokemon, False)
        else:
            return function_name(player, self.pokemon2, False)
    # return { item: lambda: function_name(player, pokemon, False) }.get(item, lambda: None)()

    def check_adicional_effect(self, pokemon1: Pokemon, pokemon2: Pokemon, attack: Attack):
        if attack.name in MOVES_CAN_CONFUSE:
            name = str(attack.name).lower().replace(' ', '_')
            function_name = getattr(Attack, name)
            
            if attack.name == 'CHATTER':
                pokemon = pokemon2
            
            
            return function_name(Attack, pokemon)
        

    def execute_command(self, command: Command, player: Player, pokemon1: Pokemon, pokemon2: Pokemon):
    
        if pokemon1.current_hp == 0:
            return None
        
        attack = None 

        # Change pokemon in battle
        if POKEMON in command.action.keys(): 

            global is_set_atk1, is_set_atk2, is_set_spatk1, is_set_spatk2, is_set_speed1, is_set_speed2, is_set_spdef1, is_set_spdef2

            # Send current pokemon to pokeball
            pokemon1.in_use = False 
            UI().delay_print(player.name + ": " +pokemon1.name + " go back")            
            # Changed pokemon
            pokemon1 = player.pokemons[command.action[POKEMON]]
            # Send to battle
            pokemon1.in_use = True             
            UI().delay_print("Let's go, " + pokemon1.name + "!")

            # Reset status to apply weather conditions to the changed pokemon
            is_set_atk1 = False
            is_set_atk2 = False
            is_set_spatk1 = False
            is_set_spatk2 = False
            is_set_speed1 = False
            is_set_speed2 = False
            is_set_spdef1 = False
            is_set_spdef2 = False  

        elif BAG in command.action.keys():  
            # Using Item from the Bag (Player) 
            if command.action[BAG][NAME] not in ('Ether', 'Max Ether'): 
                pokemon1 = self.get_item(command.action[BAG][NAME], player, pokemon1)                       

        elif ATTACK in command.action.keys():
            # Pokemon1 attack
            if command.action[ATTACK] != -1:
                move = pokemon1.attacks[command.action[ATTACK]]
                attack = Attack(move.name, move.ztype, move.category, move.power, move.accuracy, move.pp, move.stage)
            else:
                UI().delay_print(pokemon1.name + " has no moves left!")
                attack = Attack("STRUGGLE", NORMAL, PHYSICAL, 50, 100, 1, STAGE_0)

            pokemon1.last_move = attack

            self.get_pre_battle_weather_condition(pokemon1, pokemon2, attack)

            # Damage calculation
            damage_to_pokemon2 = self.compute_damage(pokemon1, attack, pokemon2)  
            self.print_damage(pokemon1, pokemon2, attack, damage_to_pokemon2)

            # Check for move adicional effects
            self.check_adicional_effect(pokemon1, pokemon2, attack)
            
            # Check if berry is held and use it if it is necesary
            self.held_berry(self.pokemon1)

    def execute_turn(self, turn: Turn):        

        self.get_pre_turn_weather_condition(self.pokemon1, self.pokemon2)    
                    
        # Determine first attacker by speed stat
        # if pokemon1 speed is greater than pokemon2 speed then pokemon1 moves first
        # if pokemon2 speed is greater than pokemon1 speed then pokemon2 moves first      
        is_first = 1
        if self.pokemon2.stats[SPEED] > self.pokemon1.stats[SPEED]:
            is_first = 2  
                  
        if is_first == 1:
            # Get commands selected
            if POKEMON not in turn.command1.action.keys() and POKEMON in turn.command2.action.keys():
                self.execute_command(turn.command2, self.player2, self.pokemon2, self.pokemon1)    
                self.execute_command(turn.command1, self.player1, self.pokemon1, self.pokemon2)
            else:
                self.execute_command(turn.command1, self.player1, self.pokemon1, self.pokemon2)
                self.execute_command(turn.command2, self.player2, self.pokemon2, self.pokemon1)   
        else:
            # Get commands selected
            if POKEMON not in turn.command1.action.keys() and POKEMON in turn.command2.action.keys():
                self.execute_command(turn.command2, self.player2, self.pokemon2, self.pokemon1)    
                self.execute_command(turn.command1, self.player1, self.pokemon1, self.pokemon2)
            else:
                self.execute_command(turn.command2, self.player2, self.pokemon2, self.pokemon1)
                self.execute_command(turn.command1, self.player1, self.pokemon1, self.pokemon2)   
                    
        self.get_post_battle_weather_condition(self.pokemon1, self.pokemon2)

        # Increment turn
        self.actual_turn += 1
              
    def print_effectiveness(self):
        global type_effectiveness

        return  {
            0: "It's not effective!",
            0.5: "It's not very effective!",
            2: "It's super effective!"
        }.get(type_effectiveness)
          
    # Print the damage caused by pokemon1
    def print_damage(self, pokemon1: Pokemon, pokemon2: Pokemon, attack: Attack, damage: int):
        global is_critical_attack, type_effectiveness

        if damage > 0:
            # Get damage multiplier
            multiplier = self.damage_multiplier_by_berry_held(pokemon2.held, pokemon2, attack)                  
            
            total_damage = int(damage * multiplier)
            
            pokemon2.current_hp -= total_damage
            
            if pokemon2.current_hp < 0:
                pokemon2.current_hp = 0
                pokemon2.current_status = ST_FAINTED            
                  
            UI().delay_print(pokemon1.name + " used " + attack.name + " and injured " + pokemon2.name + " by " + str(total_damage) + " HP")
            
            if type_effectiveness != 1:
                UI().delay_print(self.print_effectiveness())

            if is_critical_attack:
                UI().delay_print("It's a critical attack!")       
                                                                                          
            # Pokemon has no more moves left so automatically use Struggle and get recoiled
            if attack.name == 'STRUGGLE':
                UI().delay_print(pokemon1.name + " is damaged by recoil!")
                
                pokemon1.current_hp -= int(damage / 2)
                if pokemon1.current_hp < 0:
                    pokemon1.current_hp = 0
                
        elif damage == -1:
            UI().delay_print(pokemon1.name + " used " + attack.name)
        else:
            UI().delay_print(pokemon1.name + " used " + attack.name + " but missed the attack!")

    def damage_multiplier_by_berry_held(self, berry: str, pokemon: Pokemon, attack: Attack):
        # multiplier applied to damage formula
        #   1: When normal damage is dealt
        #   1/2: When pokemon2 held a berry in BERRY_CONDITIONS
        #   1/4: When pokemon2 has Ripen ability        
                
        if berry not in BERRY_CONDITIONS:
            # multiplier = 1 (No damage reduction)
            return 1
        
        if type_effectiveness > 1 and attack.ztype == BERRY_CONDITIONS[berry]:
            pokemon.held = None
            pokemon.last_berry_used = berry
            
            # pokemon2 held a berry in BERRY_CONDITIONS
            multiplier = 1/2
            
            if 'RIPEN' in (pokemon.ability[FIRST], pokemon.ability[SECOND], pokemon.ability[HIDDEN]):
                # When pokemon2 has Ripen ability
                multiplier = 1/4
                UI().delay_print(pokemon.name + " has consumed one "+ berry) 
                UI().delay_print(pokemon.name + "'s Ripen ability decreases damage!")
            else:
                UI().delay_print(pokemon.name + " has consumed one " + berry + " and the damage is halved!")    
        
        return multiplier        

    # Status of the turn
    def print_current_status(self):
        print("\nTurn: " + str(self.actual_turn))
        print(self.pokemon1.name + " has "+ str(self.pokemon1.current_hp) + "/" + str(self.pokemon1.stats[HP]) + " HP")
        print(self.pokemon2.name + " has "+ str(self.pokemon2.current_hp) + "/" + str(self.pokemon2.stats[HP]) + " HP")

    def compute_ev_earned(self, winner: Pokemon, defeated: Pokemon):
        global db_base_ev_list

        # Get Base Exp and EVs yield by pokemon name
        try:    
            with open(path_base_ev, 'r') as baseExp_EV:
                content = baseExp_EV.read()
                db_base_ev_list = loads(content)      
        except Exception:
                db_base_ev_list  = None 

        # Stats from pokemon
        stats_array = [HP, ATTACK, DEFENSE, SPATTACK, SPDEFENSE, SPEED]

        # Compute gained ev by stat
        for stat in stats_array:
            if winner.ev[stat] < 252:
                winner.ev[stat] += db_base_ev_list[defeated.name][stat+"_YIELD"]      

    def check_winner(self, pokemon1: Pokemon, pokemon2: Pokemon):
        finish = True
        UI().delay_print("\n"+pokemon1.name + " won in " + str(self.actual_turn) + " turns!")

        self.compute_ev_earned(pokemon1, pokemon2)

        # Level up 
        if pokemon1.level < 100:
            exp_gained = self.compute_experience_gained(pokemon1, pokemon2)
            UI().delay_print(pokemon1.name + " earned " + str(exp_gained) + " EXP")
            pokemon1.current_exp += exp_gained

            # Calculate amount of exp when level up
            while finish:
                if pokemon1.current_exp >= pokemon1.exp_next_level and pokemon1.level < 100:
                    excess = pokemon1.current_exp - pokemon1.exp_next_level
                    pokemon1.current_exp = excess
                    pokemon1.level += 1
                    pokemon1.get_growning_type_exp()

                    UI().delay_print(pokemon1.name + " has reached level "+ str(pokemon1.level))
                    
                    self.search_for_new_move_to_learn(pokemon1)                                                                          
                                
                else:
                    finish = False

            if pokemon1.check_evolution(pokemon1):
                UI().delay_print("\nWhat?\n" + pokemon1.name + " it's evolving\n")
                interval = time() + 10
                tick = time()
                answer = None

                # If player press B key in a time interval of 10 seconds the pokemon doesn't evolve
                while tick < interval:  
                    try: 
                        if is_pressed('b') or is_pressed('B'):  # if key 'b' is pressed 
                            answer = 'b'
                            break  
                    except:
                        break  
                    
                    tick = time()                                                                                                                                                                                                                                               

                if answer not in ['b','B']:
                    pokemon_index = self.player1.pokemons.index(pokemon1)
                    pokemon1 = pokemon1.do_evolution(pokemon1)
                    self.player1.pokemons.pop(pokemon_index)
                    self.player1.pokemons.insert(pokemon_index, pokemon1)
                    
                else:
                    UI().delay_print("Huh?\n" + pokemon1.name + " stopped evolving!\n")

            pokemon1.compute_stats()

            # Money earned
            money_earned = self.player2.money_base * pokemon2.level
            self.player1.money += money_earned
            UI().delay_print(self.player1.name + " earned "+ str(money_earned) + "$")

    # Print winner pokemon + check level up + check if can evolve
    def print_winner(self):
        global is_evolving, db_base_ev_list, db_attack_list

        # Get the moves list
        try:
            with open(path_attacks, 'r') as attacks:
                content = attacks.read()
                db_attack_list = loads(content) 
        except Exception:
                db_attack_list = None 

        
        # finish = True
        if self.pokemon2.current_hp <= 0 < self.pokemon1.current_hp:
            self.check_winner(self.pokemon1, self.pokemon2)
        elif self.pokemon1.current_hp <= 0 < self.pokemon2.current_hp:
            self.check_winner(self.pokemon2, self.pokemon1)
        else:
            UI().delay_print("Double KO in " + str(self.actual_turn) + " turns!")
        
    # Get experience gained by pokemon winner
    def compute_experience_gained(self, winner: Pokemon, fainted: Pokemon):
        # affection = 1.2 if Pokemon has an affection of two hearts or more, 1 otherwise
        affection = 1 
        
        # can_evolve = 1.2 if the winning Pokémon is at or past the level where it would be able to evolve, but it has not, 1 otherwise
        can_evolve = 1
        evo_condition = str(winner.evolution['CONDITION'])
        if evo_condition.isnumeric():
            if winner.level >= int(evo_condition):
                can_evolve = 1.2    

        # share_exp = 1 when calculating the experience of a Pokémon that participated in battle
        #             2 when calculating the experience of a Pokémon that did not participate in battle and if Exp. Share is turned on
        share_exp = 1
        if winner.held == 'EXP. SHARE': # This should be an Item() class
            share_exp = 2

        # point_power = 1 if no Exp. Point Power (Pass PowerGen V, O-PowerGen VI, Rotom PowerUSUM) is active
        #               If an Exp. Point Power is active.
        #                  0.5 for ↓↓↓, 0.66 for ↓↓, 0.8 for ↓, 1.2 for ↑, 1.5 for ↑↑, or 2 for ↑↑↑, S, or MAX
        #                  1.5 for Roto Exp. Points
        point_power = 1

        # master = 1 if the winning Pokémon's current owner is its Original Trainer
        #          1.5 if the Pokémon was gained in a domestic trade
        #          1.7 if the Pokémon was gained in an international trade (in Generation V+, this is instead approximated very closely as 6963/4096)
        master = winner.master

        # lucky_egg = 1.5 if the winning Pokémon is holding a Lucky Egg, 1 otherwise
        lucky_egg = 1
        if winner.held == 'LUCKY EGG':
            lucky_egg = 1.5
        
        exp_gained = ( fainted.base_exp * fainted.level * affection * can_evolve / (5 * share_exp) )
        exponent = pow( ( (2 * fainted.level + 10) / ( fainted.level + winner.level + 10 ) ), 2.5 )

        return int( exp_gained * exponent * master * lucky_egg * point_power )
    
    def search_for_new_move_to_learn(self, pokemon: Pokemon):
        # Search if there's a move to learn at the current level in learnsets.json
        move = None
        level = str(pokemon.level) 
        if level in pokemon.learnset["LEVEL"]:  
            move_name = str(pokemon.learnset["LEVEL"][level]).upper()                                  
            
            move = Attack( 
                move_name,
                db_attack_list[move_name][TYPE], 
                db_attack_list[move_name][CATEGORY], 
                int(db_attack_list[move_name][POWER]), 
                int(db_attack_list[move_name][ACCURACY]), 
                int(db_attack_list[move_name][PP]),
                STAGE_0
            )
            
            if len(pokemon.attacks) < 4:
                pokemon.attacks.insert(len(pokemon.attacks) + 1, move)
                UI().delay_print(pokemon.name + " has learned " + move_name)
            else:
                while True:
                    UI().delay_print(pokemon.name + " wants to learn the move " + move_name)
                    UI().delay_print("But " + pokemon.name + " can't learn more than four moves")
                    UI().delay_print("Make forget another move?")
                    
                    while True:
                        answer = str(input()).upper()
                        if answer in ['YES', 'Y', 'NO', 'N']:
                            break
                    
                    if answer in ['YES', 'Y']:
                        # Learn new move                                                                               
                        while True:                                            
                            UI().delay_print("What move should " + pokemon.name + " forget?")
                            i = 0
                            for attack in pokemon.attacks:
                                print(str(i) + ". " + attack.name)
                                i += 1
                                                                            
                            answer = input()
                            if answer.isnumeric():
                                if int(answer) in range(0, i):
                                    index = int(answer)
                                    UI().delay_print("Do you want to forget " + pokemon.attacks[index].name + "?")
                                    
                                    while True:
                                        answer = str(input()).upper()
                                        if answer in ['YES', 'Y', 'NO', 'N']:
                                            break
                                    
                                    if answer in ['YES', 'Y']:           
                                        UI().delay_print(pokemon.name + " forgot " + pokemon.attacks[index].name)                                             
                                        pokemon.attacks.pop(index)
                                        
                                        UI().delay_print("And learned " + move_name)
                                        pokemon.attacks.insert(index, move)
                                        break
                            
                        break
                    else:
                        UI().delay_print("Well then, should " + pokemon.name + " give up on learning " + move_name)
                        while True:
                            answer = str(input()).upper()
                            if answer in ['YES', 'Y', 'NO', 'N']:
                                break 
                        
                        if answer in ['YES', 'Y']:
                            UI().delay_print(pokemon.name + " did not learn " + move_name)
                            break
    
    def held_berry(self, pokemon: Pokemon):
        if pokemon.held == 'Cheri Berry' and pokemon.current_status == ST_PARALYZED:
            pokemon.held = None
            pokemon.current_status = ST_NORMAL
            pokemon.last_berry_used = 'Cheri Berry'

            UI().delay_print(pokemon.name + " has consumed a held Cheri Berry")
            UI().delay_print(pokemon.name + " is not paralyzed!")
            return pokemon

        if pokemon.held == 'Chesto Berry' and pokemon.current_status == ST_SLEEP:
            pokemon.held = None
            pokemon.current_status = ST_NORMAL
            pokemon.last_berry_used = 'Chesto Berry'

            UI().delay_print(pokemon.name + " has consumed a held Chesto Berry")
            UI().delay_print(pokemon.name + " has woken up!")
            return pokemon

        if pokemon.held == 'Pecha Berry' and pokemon.current_status in (ST_POISONED, ST_BADLYPOISON):
            pokemon.held = None
            pokemon.current_status = ST_NORMAL
            pokemon.last_berry_used = 'Pecha Berry'

            UI().delay_print(pokemon.name + " has consumed a held Pecha Berry")
            UI().delay_print(pokemon.name + " has been cured from poisoning!")
            return pokemon

        if pokemon.held == 'Rawst Berry' and pokemon.current_status == ST_BURNED:
            pokemon.held = None
            pokemon.current_status = ST_NORMAL
            pokemon.last_berry_used = 'Rawst Berry'

            UI().delay_print(pokemon.name + " has consumed a held Rawst Berry")
            UI().delay_print(pokemon.name + " has been cured from burning!")
            return pokemon

        if pokemon.held == 'Aspear Berry' and pokemon.current_status == ST_FREEZED:
            pokemon.held = None
            pokemon.current_status = ST_NORMAL
            pokemon.last_berry_used = 'Aspeart Berry'

            UI().delay_print(pokemon.name + " has consumed a held Aspear Berry")
            UI().delay_print(pokemon.name + " is no longer freezed!")
            return pokemon

        if pokemon.held == 'Leppa Berry':
            for move in pokemon.attacks:
                if move.name == pokemon.last_move.name and move.pp == 0:
                    move.pp += 10
                    pokemon.held = None
                    pokemon.last_berry_used = 'Leppa Berry'

                    UI().delay_print(pokemon.name + " has consumed a held Leppa Berry")
                    UI().delay_print("10 PP has been restored from " + move.name)
            return pokemon

        if pokemon.held == 'Oran Berry' and pokemon.current_hp < int(pokemon.stats[HP] / 2):
            # Due to a glitch, dropping below half HP by taking self-inflicted 
            # damage from confusion will not activate the Oran Berry.
            pokemon.current_hp += 10
            pokemon.held = None
            pokemon.last_berry_used = 'Oran Berry'

            UI().delay_print(pokemon.name + " has consumed a held Oran Berry")
            UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
            return pokemon

        if pokemon.held == 'Persim Berry' and pokemon.current_status == ST_CONFUSION:
            pokemon.current_status = ST_NORMAL
            pokemon.held = None
            pokemon.last_berry_used = 'Persim Berry'

            UI().delay_print(pokemon.name + " has consumed a held Persim Berry")
            UI().delay_print(pokemon.name + " is no longer confused!")
            return pokemon

        status = (ST_POISONED, ST_BADLYPOISON, ST_FREEZED, ST_PARALYZED, ST_SLEEP, ST_CONFUSION)
        if pokemon.held == 'Lum Berry' and pokemon.current_status in status:
            pokemon.current_status = ST_NORMAL
            pokemon.held = None
            pokemon.last_berry_used = 'Lum Berry'

            UI().delay_print(pokemon.name + " has consumed a held Lum Berry")
            UI().delay_print(pokemon.name + " has been fully cured!")
            return pokemon     

        if pokemon.held == 'Sitrus Berry' and pokemon.current_hp < int(pokemon.stats[HP] / 2):
            # Due to a glitch, dropping below half HP by taking self-inflicted 
            # damage from confusion will not activate the Oran Berry.
            pokemon.current_hp += int(pokemon.stats[HP] / 4)
            pokemon.held = None
            pokemon.last_berry_used = 'Sitrus Berry'

            UI().delay_print(pokemon.name + " has consumed a held Sitrus Berry")
            UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
            return pokemon      

        if pokemon.held == 'Figy Berry' and pokemon.current_hp < int(pokemon.stats[HP] / 2):
            pokemon.current_hp += int(pokemon.stats[HP] / 8)
            pokemon.held = None
            pokemon.last_berry_used = 'Figy Berry'

            UI().delay_print(pokemon.name + " has consumed a held Figy Berry")
            UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
            
            if pokemon.nature in FLAVOR_DISLIKE[SPICY] and FLAVOR_DISLIKE[SPICY][pokemon.nature] == DF:
                pokemon.current_status = ST_CONFUSION
                UI().delay_print("But " + pokemon.name + " doesn't like the taste and gets confused!")
                
            return pokemon
        
        if pokemon.held == 'Wiki Berry' and pokemon.current_hp < int(pokemon.stats[HP] / 2):
            pokemon.current_hp += int(pokemon.stats[HP] / 8)
            pokemon.held = None
            pokemon.last_berry_used = 'Wiki Berry'

            UI().delay_print(pokemon.name + " has consumed a held Wiki Berry")
            UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
            
            if pokemon.nature in FLAVOR_DISLIKE[DRY] and FLAVOR_DISLIKE[DRY][pokemon.nature] == DF:
                pokemon.current_status = ST_CONFUSION
                UI().delay_print("But " + pokemon.name + " doesn't like the taste and gets confused!")
                
            return pokemon
        
        if pokemon.held == 'Mago Berry' and pokemon.current_hp < int(pokemon.stats[HP] / 2):
            pokemon.current_hp += int(pokemon.stats[HP] / 8)
            pokemon.held = None
            pokemon.last_berry_used = 'Mago Berry'

            UI().delay_print(pokemon.name + " has consumed a held Mago Berry")
            UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
            
            if pokemon.nature in FLAVOR_DISLIKE[SWEET] and FLAVOR_DISLIKE[SWEET][pokemon.nature] == DF:
                pokemon.current_status = ST_CONFUSION
                UI().delay_print("But " + pokemon.name + " doesn't like the taste and gets confused!")
                
            return pokemon
        
        if pokemon.held == 'Aguav Berry' and pokemon.current_hp < int(pokemon.stats[HP] / 2):
            pokemon.current_hp += int(pokemon.stats[HP] / 8)
            pokemon.held = None
            pokemon.last_berry_used = 'Aguav Berry'

            UI().delay_print(pokemon.name + " has consumed a held Aguav Berry")
            UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
            
            if pokemon.nature in FLAVOR_DISLIKE[BITTER] and FLAVOR_DISLIKE[BITTER][pokemon.nature] == DF:
                pokemon.current_status = ST_CONFUSION
                UI().delay_print("But " + pokemon.name + " doesn't like the taste and gets confused!")
                
            return pokemon 
        
        if pokemon.held == 'Lapapa Berry' and pokemon.current_hp < int(pokemon.stats[HP] / 2):
            pokemon.current_hp += int(pokemon.stats[HP] / 8)
            pokemon.held = None
            pokemon.last_berry_used = 'Lapapa Berry'

            UI().delay_print(pokemon.name + " has consumed a held Lapapa Berry")
            UI().delay_print(pokemon.name + " HP "+ str(pokemon.current_hp))
            
            if pokemon.nature in FLAVOR_DISLIKE[SOUR] and FLAVOR_DISLIKE[SOUR][pokemon.nature] == DF:
                pokemon.current_status = ST_CONFUSION
                UI().delay_print("But " + pokemon.name + " doesn't like the taste and gets confused!")
                
            return pokemon                         

    def pre_turn_harsh_sunlight(self, pokemon1: Pokemon, pokemon2: Pokemon): 
        global is_set_spatk1, is_set_spatk2, is_set_atk1, is_set_atk2

        if 'SOLAR POWER' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and not is_set_spatk1: 
            pokemon1.stats[SPATTACK] = int(pokemon1.stats[SPATTACK] * 1.5)
            is_set_spatk1 = True

        if 'SOLAR POWER' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and not is_set_spatk2: 
            pokemon2.stats[SPATTACK] = int(pokemon2.stats[SPATTACK] * 1.5)
            is_set_spatk2 = True

        if 'FLOWER GIFT' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and not is_set_atk1:           
            pokemon1.stats[ATTACK] = int(pokemon1.stats[ATTACK] * 1.5)
            pokemon1.stats[SPDEFENSE] = int(pokemon1.stats[SPDEFENSE] * 1.5)
            is_set_atk1 = True            

        if 'FLOWER GIFT' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and not is_set_atk2: 
            pokemon2.stats[ATTACK] = int(pokemon2.stats[ATTACK] * 1.5)
            pokemon2.stats[SPDEFENSE] = int(pokemon2.stats[SPDEFENSE] * 1.5)
            is_set_atk2 = True    


        if 'FORECAST' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and pokemon1.name == 'Castform': 
            # Change Castform to Rainy Form (Water-type)
            pass
                
        if 'FORECAST' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and pokemon2.name == 'Castform':  
            #C hange Castform to Rainy Form (Water-type)
            pass  

    def pre_battle_harsh_sunlight(self, pokemon1: Pokemon, attack: Attack):
        if attack.ztype == FIRE:
            attack.power *= 1.5
        
        if attack.ztype == WATER:
            attack.power *= 0.5

        if attack.name in ('SOLAR BEAN', 'SOLAR BLADE'):
            attack.turns_to_execute = 1
        
        if attack.name == 'WEATHER BALL':
            attack.ztype = FIRE
            attack.power *= 2
        
        # Reduce accurary of thunder and hurricane from 70% to 50%
        if attack.name in ('THUNDER', 'HURRICANE'):
            attack.accuracy = 50

        # prevent pokemon to get Frozen
        if not pokemon1.cant_be_affected_by.__contains__(ST_FREEZED):
            pokemon1.cant_be_affected_by.append(ST_FREEZED)
        
        if 'LEAF GUARD' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and attack.name == 'REST':
            attack.accuracy = 0

        if attack.name == 'GROWTH':
            pokemon1.stats[ATTACK] = int(pokemon1.stats[ATTACK] / STAT_STAGE_MULTIPLIER[pokemon1.stats_stages[ATTACK]])
            pokemon1.stats_stages[ATTACK] += 2
            if pokemon1.stats_stages[ATTACK] > 6:
                pokemon1.stats_stages[ATTACK] = 6     

            pokemon1.stats[ATTACK] = int(pokemon1.stats[ATTACK] * STAT_STAGE_MULTIPLIER[pokemon1.stats_stages[ATTACK]])

            pokemon1.stats[SPATTACK] = int(pokemon1.stats[SPATTACK] / STAT_STAGE_MULTIPLIER[pokemon1.stats_stages[SPATTACK]])
            pokemon1.stats_stages[SPATTACK] += 2
            if pokemon1.stats_stages[SPATTACK] > 6:
                pokemon1.stats_stages[SPATTACK] = 6

            pokemon1.stats[SPATTACK] = int(pokemon1.stats[SPATTACK] * STAT_STAGE_MULTIPLIER[pokemon1.stats_stages[SPATTACK]])

    def post_battle_harsh_sunlight(self, pokemon1: Pokemon, pokemon2: Pokemon):
        if 'LEAF GUARD' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            if not pokemon1.cant_be_affected_by.__contains__(ST_BURNED):
                pokemon1.cant_be_affected_by.append(ST_BURNED)
            if not pokemon1.cant_be_affected_by.__contains__(ST_PARALYZED):
                pokemon1.cant_be_affected_by.append(ST_PARALYZED) 
            if not pokemon1.cant_be_affected_by.__contains__(ST_POISONED):
                pokemon1.cant_be_affected_by.append(ST_POISONED) 
            if not pokemon1.cant_be_affected_by.__contains__(ST_BADLYPOISON):
                pokemon1.cant_be_affected_by.append(ST_BADLYPOISON) 
            if not pokemon1.cant_be_affected_by.__contains__(ST_SLEEP):   
                pokemon1.cant_be_affected_by.append(ST_SLEEP) 

        if 'LEAF GUARD' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]):
            if not pokemon2.cant_be_affected_by.__contains__(ST_BURNED):
                pokemon2.cant_be_affected_by.append(ST_BURNED)
            if not pokemon2.cant_be_affected_by.__contains__(ST_PARALYZED):
                pokemon2.cant_be_affected_by.append(ST_PARALYZED) 
            if not pokemon2.cant_be_affected_by.__contains__(ST_POISONED):
                pokemon2.cant_be_affected_by.append(ST_POISONED) 
            if not pokemon2.cant_be_affected_by.__contains__(ST_BADLYPOISON):
                pokemon2.cant_be_affected_by.append(ST_BADLYPOISON) 
            if not pokemon2.cant_be_affected_by.__contains__(ST_SLEEP):   
                pokemon2.cant_be_affected_by.append(ST_SLEEP)         

        if 'HARVEST' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pokemon1.held = pokemon1.last_berry_used
            UI().delay_print(pokemon1.name + "'s Harvest!")
            UI().delay_print(pokemon1.name + " recovered " + pokemon1.last_berry_used)

        if 'HARVEST' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]):
            pokemon2.held = pokemon2.last_berry_used
            UI().delay_print(pokemon2.name + "'s Harvest!")
            UI().delay_print(pokemon2.name + " recovered " + pokemon2.last_berry_used)            
        
        if pokemon1.last_move != None and pokemon1.last_move.name in ('MOONLIGHT', 'SYNTHESIS', 'MORNING SUN'):
            recovery = int(pokemon1.stats[HP] * (2/3))
            if recovery < 1:
                pokemon1.current_hp += 1
            else:
                pokemon1.current_hp += recovery
            
            if pokemon1.current_hp > pokemon1.stats[HP]:
                pokemon1.current_hp = pokemon1.stats[HP]   

        if pokemon2.last_move != None and pokemon2.last_move.name in ('MOONLIGHT', 'SYNTHESIS', 'MORNING SUN'):
            recovery = int(pokemon2.stats[HP] * (2/3))
            if recovery < 1:
                pokemon2.current_hp += 1
            else:
                pokemon2.current_hp += recovery
            
            if pokemon2.current_hp > pokemon2.stats[HP]:
                pokemon2.current_hp = pokemon2.stats[HP]                  

        # DRY SKIN ability
        if 'DRY SKIN' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]): 
            pokemon1.current_hp -= int(pokemon1.stats[HP] * (1/8))
            if pokemon1.current_hp < 0:
                pokemon1.current_hp = 0
            UI().delay_print(pokemon1.name + "'s Dry Skin!")
                
        if 'DRY SKIN' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]): 
            pokemon2.current_hp -= int(pokemon2.stats[HP] * (1/8))
            if pokemon2.current_hp < 0:
                pokemon2.current_hp = 0
            UI().delay_print(pokemon2.name + "'s Dry Skin!")        
        
        # SOLAR POWER ability
        if 'SOLAR POWER' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]): 
            pokemon1.current_hp -= int(pokemon1.stats[HP] * (1/8))
            if pokemon1.current_hp < 0:
                pokemon1.current_hp = 0
            UI().delay_print(pokemon1.name + " is affected by Solar Power!") 
                
        if 'SOLAR POWER' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]): 
            pokemon2.current_hp -= int(pokemon2.stats[HP] * (1/8))
            if pokemon2.current_hp < 0:
                pokemon2.current_hp = 0 
            UI().delay_print(pokemon2.name + " is affected by Solar Power!")                       

    def pre_battle_extremely_harsh_sunlight(self, pokemon1: Pokemon, attack: Attack):

        self.pre_battle_harsh_sunlight(pokemon1, attack)

        if attack.ztype == WATER:
            attack.accuracy = 0
        
        if attack.name in ('SUNNY DAY', 'RAIN DANCE', ' SANDSTORM', 'HAIL'): # CLOUD NINE/ AIR LOCK doesn't affect
            attack.accuracy = 0

    def post_battle_extremely_harsh_sunlight(self, pokemon1: Pokemon, pokemon2: Pokemon):

        self.post_battle_harsh_sunlight(pokemon1, pokemon2)

        if pokemon1.last_move != None and pokemon1.last_move.name == 'SUNNY DAY' and pokemon1.affected_by == 'POWDER': # GEN VI onward
            pokemon1.current_hp -= int(pokemon1.stats[HP] * (1/4))

        if pokemon2.last_move != None and pokemon2.last_move.name == 'SUNNY DAY' and pokemon2.affected_by == 'POWDER': # GEN VI onward
            pokemon2.current_hp -= int(pokemon2.stats[HP] * (1/4))

        if str(pokemon1.held).find("Berry") and pokemon1.last_move != None and pokemon1.last_move.name == 'NATURAL GIFT':
            # TODO
            pokemon1.held = pokemon1.last_berry_used 

        if str(pokemon1.held).find("Berry") and pokemon2.last_move != None and pokemon2.last_move.name == 'NATURAL GIFT':
            # TODO
            pokemon1.held = pokemon1.last_berry_used             
        
        if pokemon1.current_status == ST_FREEZED and pokemon1.last_move != None and pokemon1.last_move.name in ('SCALD', 'STEAM ERUPTION'):
            pokemon1.current_status = ST_NORMAL   

        if pokemon1.current_status == ST_FREEZED and pokemon2.last_move != None and pokemon2.last_move.name in ('SCALD', 'STEAM ERUPTION'):
            pokemon2.current_status = ST_NORMAL               

        if 'DROUGHT' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pass # FAIL # CLOUD NINE/ AIR LOCK doesn't affect

        if 'DRIZZLE' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pass # FAIL # CLOUD NINE/ AIR LOCK doesn't affect

        if 'SAND STREAM' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pass # FAIL # CLOUD NINE/ AIR LOCK doesn't affect
        
        if 'SNOW WARNING' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pass # FAIL # CLOUD NINE/ AIR LOCK doesn't affect#

    def pre_turn_rain(self, pokemon1: Pokemon, pokemon2: Pokemon):
        global is_set_speed1, is_set_speed2

        # Ability changes while Harsh Sunlight/Extremely Harsh Sunglight
        if 'SWIFT SWIM' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and not is_set_speed1:
            pokemon1.stats[SPEED] *= 2
            is_set_speed1 = True
            
        if 'SWIFT SWIM' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and not is_set_speed2:
            pokemon2.stats[SPEED] *= 2   
            is_set_speed2 = True
                        
        if 'FORECAST' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and pokemon1.name == 'Castform': 
            # Change Castform to Rainy Form (Water-type)
            pass
                
        if 'FORECAST' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and pokemon2.name == 'Castform':  
            #C hange Castform to Rainy Form (Water-type)
            pass     

    def pre_battle_rain(self, attack: Attack):
        if attack.ztype == FIRE:
            attack.power *= 0.5
        
        if attack.ztype == WATER:
            attack.power *= 1.5

        if attack.name in ('SOLAR BEAN', 'SOLAR BLADE'):
            attack.turns_to_execute = 2
            attack.power = int(attack.power / 2)
        
        if attack.name == 'WEATHER BALL':
            attack.ztype = WATER
            attack.power *= 2
        
        # Bypass the accurary check of thunder and hurricane
        if attack.name in ('THUNDER', 'HURRICANE'):
            attack.accuracy = 100

    def post_battle_rain(self, pokemon1: Pokemon, pokemon2: Pokemon):           
        
        if pokemon1.last_move != None and pokemon1.last_move.name in ('MOONLIGHT', 'SYNTHESIS', 'MORNING SUN'):
            recovery = int(pokemon1.stats[HP] * (1/4))
            if recovery < 1:
                pokemon1.current_hp += 1
            else:
                pokemon1.current_hp += recovery
            
            if pokemon1.current_hp > pokemon1.stats[HP]:
                pokemon1.current_hp = pokemon1.stats[HP]   

        if pokemon2.last_move != None and pokemon2.last_move.name in ('MOONLIGHT', 'SYNTHESIS', 'MORNING SUN'):
            recovery = int(pokemon2.stats[HP] * (1/4))
            if recovery < 1:
                pokemon2.current_hp += 1
            else:
                pokemon2.current_hp += recovery
            
            if pokemon2.current_hp > pokemon2.stats[HP]:
                pokemon2.current_hp = pokemon2.stats[HP]                  

        # DRY SKIN ability
        if 'DRY SKIN' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]): 
            pokemon1.current_hp += int(pokemon1.stats[HP] * (1/8))
            if pokemon1.current_hp > pokemon1.stats[HP]:
                pokemon1.current_hp = pokemon1.stats[HP]
            UI().delay_print(pokemon1.name + "'s Dry Skin!")
                
        if 'DRY SKIN' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]): 
            pokemon2.current_hp += int(pokemon2.stats[HP] * (1/8))
            if pokemon1.current_hp > pokemon2.stats[HP]:
                pokemon1.current_hp = pokemon2.stats[HP]
            UI().delay_print(pokemon2.name + "'s Dry Skin!")        
        
        if 'HYDRATION' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            if pokemon1.current_status in (ST_BURNED, ST_FREEZED, ST_PARALYZED, ST_POISONED, ST_BADLYPOISON, ST_SLEEP, 'ST_DROWSY'):
                pokemon1.current_status = ST_NORMAL  

        if 'HYDRATION' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]):
            if pokemon2.current_status in (ST_BURNED, ST_FREEZED, ST_PARALYZED, ST_POISONED, ST_BADLYPOISON, ST_SLEEP, 'ST_DROWSY'):
                pokemon2.current_status = ST_NORMAL  

        if 'RAIN DISH' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pokemon1.current_hp += int(pokemon1.stats[HP] * (1/16))
            if pokemon1.current_hp > pokemon1.stats[HP]:
                pokemon1.current_hp = pokemon1.stats[HP]
            UI().delay_print(pokemon1.name + "'s Rain Dis!")

        if 'RAIN DISH' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]):
            pokemon2.current_hp += int(pokemon2.stats[HP] * (1/16))
            if pokemon1.current_hp > pokemon2.stats[HP]:
                pokemon1.current_hp = pokemon2.stats[HP]
            UI().delay_print(pokemon2.name + "'s Rain Dish!")

    def pre_battle_heavy_rain(self, pokemon1: Pokemon, attack: Attack):

        self.pre_battle_rain(attack)

        if attack.ztype == FIRE:
            attack.accuracy = 0

        if attack.name in ('SUNNY DAY', 'RAIN DANCE', ' SANDSTORM', 'HAIL'): # CLOUD NINE/ AIR LOCK doesn't affect
            attack.accuracy = 0

        if 'DROUGHT' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pass # FAIL # CLOUD NINE/ AIR LOCK doesn't affect

        if 'DRIZZLE' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pass # FAIL # CLOUD NINE/ AIR LOCK doesn't affect

        if 'SAND STREAM' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pass # FAIL # CLOUD NINE/ AIR LOCK doesn't affect
        
        if 'SNOW WARNING' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            pass # FAIL # CLOUD NINE/ AIR LOCK doesn't affect

    def post_battle_heavy_rain(self, pokemon1: Pokemon, pokemon2: Pokemon):
        if  pokemon1.last_move != None and pokemon1.last_move.ztype == FIRE and pokemon1.affected_by == 'POWDER': # GEN VI onward
            pokemon1.current_hp -= int(pokemon1.stats[HP] * (1/4))

        if pokemon2.last_move != None and pokemon2.last_move.ztype == FIRE and pokemon2.affected_by == 'POWDER': # GEN VI onward
            pokemon2.current_hp -= int(pokemon2.stats[HP] * (1/4))

        if str(pokemon1.held).find("Berry") and pokemon1.last_move != None and pokemon1.last_move.name == 'NATURAL GIFT':
            # TODO If a Pokémon attempts to use Natural Gift while holding a Berry that makes the move Fire-type, the Berry is not consumed.
            pokemon1.held = pokemon1.last_berry_used 

        if str(pokemon1.held).find("Berry") and pokemon2.last_move != None and pokemon2.last_move.name == 'NATURAL GIFT':
            # TODO If a Pokémon attempts to use Natural Gift while holding a Berry that makes the move Fire-type, the Berry is not consumed.
            pokemon1.held = pokemon1.last_berry_used             
        
        if pokemon1.current_status == ST_FREEZED and pokemon1.last_move != None and pokemon1.last_move.ztype == FIRE:
            pokemon1.current_status = ST_NORMAL   

        if pokemon1.current_status == ST_FREEZED and pokemon2.last_move != None and pokemon2.last_move.ztype == FIRE:
            pokemon2.current_status = ST_NORMAL 

    def pre_turn_sandstorm(pokemon1: Pokemon, pokemon2: Pokemon):
        global is_set_speed1, is_set_speed2, is_set_spdef1, is_set_spdef2

        if 'SAND RUSH' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and not is_set_speed1:
            pokemon1.stats[SPEED] *= 2
            is_set_speed1 = True

        if 'SAND RUSH' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and not is_set_speed2:
            pokemon2.stats[SPEED] *= 2
            is_set_speed2 = True

        if pokemon1.type1 == ROCK or pokemon1.type2 != None and pokemon1.type2 == ROCK and not is_set_spdef1:
            pokemon1.stats[SPDEFENSE] *= 1.5
            is_set_spdef1 = True
                            
        if pokemon2.type1 == ROCK or pokemon2.type2 != None and pokemon2.type2 == ROCK and not is_set_spdef2:            
            pokemon2.stats[SPDEFENSE] *= 1.5
            is_set_spdef2 = True

    def pre_battle_sandstorm(pokemon1: Pokemon, pokemon2: Pokemon, attack: Attack):
        
        if 'SAND FORCE' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]):
            if attack.ztype in (ROCK, STEEL, GROUND):
                attack.power *= 1.3

        if attack.name == 'WEATHER BALL':
            attack.ztype = ROCK
            attack.power *= 2
        
        if attack.name in ('SOLAR BEAM', 'SOLAR BLADE'):
            attack.power = int(attack.power / 2)

        if 'SAND VEIL' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]):
            attack.accuracy = int(attack.accuracy * (4/5))

    def post_battle_sandstorm(pokemon1: Pokemon, pokemon2: Pokemon):
        sand_abilities = ('SAND FORCE', 'SAND RUSH', 'SAND VEIL', 'MAGIC GUARD', 'OVERCOAT')

        if pokemon1.type1 not in (ROCK, STEEL, GROUND) or pokemon1.type2 not in (None, ROCK, STEEL, GROUND):
            if  pokemon1.ability[FIRST] not in sand_abilities or pokemon1.ability[SECOND] not in sand_abilities or pokemon1.ability[HIDDEN] not in sand_abilities:
                if pokemon1.held != 'SAFETY GOOGLES':
                    pokemon1.current_hp *= int(pokemon1.stats[HP] * (1/16))

        if pokemon2.type1 not in (ROCK, STEEL, GROUND) or pokemon2.type2 not in (None, ROCK, STEEL, GROUND):
            if  pokemon2.ability[FIRST] not in sand_abilities or pokemon2.ability[SECOND] not in sand_abilities or pokemon2.ability[HIDDEN] not in sand_abilities:
                if pokemon2.held != 'SAFETY GOOGLES':
                    pokemon2.current_hp *= int(pokemon2.stats[HP] * (1/16))
        
        if pokemon1.last_move != None and pokemon1.last_move.name == 'SHORE UP':
            pokemon1.current_hp += int(pokemon1.stats[HP] * (2/3))
        
        if pokemon2.last_move != None and pokemon2.last_move.name == 'SHORE UP':
            pokemon2.current_hp += int(pokemon1.stats[HP] * (2/3))

        if pokemon1.last_move != None and pokemon1.last_move.name in ('MOONLIGHT', 'SYNTHESIS', 'MORNING SUN'):
            recovery = int(pokemon1.stats[HP] * (1/4))
            if recovery < 1:
                pokemon1.current_hp += 1
            else:
                pokemon1.current_hp += recovery
            
            if pokemon1.current_hp > pokemon1.stats[HP]:
                pokemon1.current_hp = pokemon1.stats[HP]   

        if pokemon2.last_move != None and pokemon2.last_move.name in ('MOONLIGHT', 'SYNTHESIS', 'MORNING SUN'):
            recovery = int(pokemon2.stats[HP] * (1/4))
            if recovery < 1:
                pokemon2.current_hp += 1
            else:
                pokemon2.current_hp += recovery
            
            if pokemon2.current_hp > pokemon2.stats[HP]:
                pokemon2.current_hp = pokemon2.stats[HP]          

    def pre_turn_hail(self, pokemon1: Pokemon, pokemon2: Pokemon):
        global is_set_speed1, is_set_speed2

        if 'SLUSH RUSH' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and not is_set_speed1:
            pokemon1.stats[SPEED] *= 2
            is_set_speed1 = True

        if 'SLUSH RUSH' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and not is_set_speed2:
            pokemon2.stats[SPEED] *= 2
            is_set_speed2 = True

        if 'FORECAST' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]) and pokemon1.name == 'Castform': 
            # Change Castform to Snowy Form (Ice-type)
            pass
                
        if 'FORECAST' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]) and pokemon2.name == 'Castform':  
            #C hange Castform to Snowy Form (Ice-type)
            pass  

    def pre_battle_hail(self, pokemon2: Pokemon, attack: Attack):
        if attack.name == 'WEATHER BALL':
            attack.ztype = ICE
            attack.power *= 2
        
        if 'SNOW CLOAK' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]):
            attack.accuracy = int(attack.accuracy * (4/5))

        # Bypass the accurary check of blizzard
        if attack.name == 'BLIZZARD':
            attack.accuracy = 100            

        if attack.name in ('SOLAR BEAM', 'SOLAR BLADE'):
            attack.power = int(attack.power / 2)

    def post_battle_hail(self, pokemon1: Pokemon, pokemon2: Pokemon):
        ice_abilities = ('ICE BODY', 'SNOW CLOAK', 'MAGIC GUARD', 'OVERCOAT')

        if ICE not in (pokemon1.type1, pokemon1.type2):
            if  pokemon1.ability[FIRST] not in ice_abilities or pokemon1.ability[SECOND] not in ice_abilities or pokemon1.ability[HIDDEN] not in ice_abilities:
                if pokemon1.held != 'SAFETY GOOGLES':
                    pokemon1.current_hp *= int(pokemon1.stats[HP] * (1/16))

        if ICE not in (pokemon2.type1, pokemon2.type2):
            if  pokemon2.ability[FIRST] not in ice_abilities or pokemon2.ability[SECOND] not in ice_abilities or pokemon2.ability[HIDDEN] not in ice_abilities:
                if pokemon2.held != 'SAFETY GOOGLES':
                    pokemon2.current_hp *= int(pokemon2.stats[HP] * (1/16))


        if 'ICE BODY' in (pokemon1.ability[FIRST], pokemon1.ability[SECOND], pokemon1.ability[HIDDEN]): 
            pokemon1.current_hp = int(pokemon1.stats[HP] * (1/16)) 
                
        if 'ICE BODY' in (pokemon2.ability[FIRST], pokemon2.ability[SECOND], pokemon2.ability[HIDDEN]):  
            pokemon2.current_hp = int(pokemon2.stats[HP] * (1/16))  

        if pokemon1.last_move != None and pokemon1.last_move.name in ('MOONLIGHT', 'SYNTHESIS', 'MORNING SUN'):
            recovery = int(pokemon1.stats[HP] * (1/4))
            if recovery < 1:
                pokemon1.current_hp += 1
            else:
                pokemon1.current_hp += recovery
            
            if pokemon1.current_hp > pokemon1.stats[HP]:
                pokemon1.current_hp = pokemon1.stats[HP]   

        if pokemon2.last_move != None and pokemon2.last_move.name in ('MOONLIGHT', 'SYNTHESIS', 'MORNING SUN'):
            recovery = int(pokemon2.stats[HP] * (1/4))
            if recovery < 1:
                pokemon2.current_hp += 1
            else:
                pokemon2.current_hp += recovery
            
            if pokemon2.current_hp > pokemon2.stats[HP]:
                pokemon2.current_hp = pokemon2.stats[HP]            
    
    # Get pre turn weather condition from weather type
    # WEATHER_TYPE = {
    #     1: "HARSH SUNLIGHT",
    #     2: "EXTREMELY HARSH SUNLIGHT",
    #     3: "RAIN",
    #     4: "HEAVY RAIN",
    #     5: "SANDSTORM",
    #     6: "HAIL"
    # }  
    def get_pre_turn_weather_condition(self, pokemon1: Pokemon, pokemon2: Pokemon):
        return {
            WEATHER_TYPE[1]: lambda: self.pre_turn_harsh_sunlight(pokemon1, pokemon2),
            WEATHER_TYPE[2]: lambda: self.pre_turn_harsh_sunlight(pokemon1, pokemon2), # To Extemely Harsh Sunlight
            WEATHER_TYPE[3]: lambda: self.pre_turn_rain(pokemon1, pokemon2),
            WEATHER_TYPE[4]: lambda: self.pre_turn_rain(pokemon1, pokemon2), # To Heavy Rain
            WEATHER_TYPE[5]: lambda: self.pre_turn_sandstorm(pokemon1, pokemon2),
            WEATHER_TYPE[6]: lambda: self.pre_turn_hail(pokemon1, pokemon2)
        }.get(self.weather, lambda: None)()
    
    # Get pre battle weather condition from weather type
    # WEATHER_TYPE = {
    #     1: "HARSH SUNLIGHT",
    #     2: "EXTREMELY HARSH SUNLIGHT",
    #     3: "RAIN",
    #     4: "HEAVY RAIN",
    #     5: "SANDSTORM",
    #     6: "HAIL"
    # }    
    def get_pre_battle_weather_condition(self, pokemon1: Pokemon, pokemon2: Pokemon, attack: Attack):
        return {
            WEATHER_TYPE[1]: lambda: self.pre_battle_harsh_sunlight(pokemon1, attack),
            WEATHER_TYPE[2]: lambda: self.pre_battle_extremely_harsh_sunlight(pokemon1, attack),
            WEATHER_TYPE[3]: lambda: self.pre_battle_rain(attack),
            WEATHER_TYPE[4]: lambda: self.pre_battle_heavy_rain(pokemon1, attack),
            WEATHER_TYPE[5]: lambda: self.pre_battle_sandstorm(pokemon1, pokemon2, attack), 
            WEATHER_TYPE[6]: lambda: self.pre_battle_hail(pokemon2, attack)                     
        }.get(self.weather, lambda: None)()

    # Get post battle weather condition from weather type
    # WEATHER_TYPE = {
    #     1: "HARSH SUNLIGHT",
    #     2: "EXTREMELY HARSH SUNLIGHT",
    #     3: "RAIN",
    #     4: "HEAVY RAIN",
    #     5: "SANDSTORM",
    #     6: "HAIL"
    # }    
    def get_post_battle_weather_condition(self, pokemon1: Pokemon, pokemon2: Pokemon):
        return {
            WEATHER_TYPE[1]: lambda: self.post_battle_harsh_sunlight(pokemon1, pokemon2),
            WEATHER_TYPE[2]: lambda: self.post_battle_extremely_harsh_sunlight(pokemon1, pokemon2),
            WEATHER_TYPE[3]: lambda: self.post_battle_rain(pokemon1, pokemon2),
            WEATHER_TYPE[4]: lambda: self.post_battle_heavy_rain(pokemon1, pokemon2),
            WEATHER_TYPE[5]: lambda: self.post_battle_sandstorm(pokemon1, pokemon2),
            WEATHER_TYPE[6]: lambda: self.post_battle_hail(pokemon1, pokemon2)                         
        }.get(self.weather, lambda: None)()              