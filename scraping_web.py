from bs4 import BeautifulSoup
from requests import *
from json import *
from constants import *
from Models.attack import *

def get_pokedex():
    url = 'https://pokemondb.net/pokedex/all'

    try:
        page_response = get(url, timeout = 5)
    except Exception:
        print('No hay conexión de internet')
        return None

    page_content = BeautifulSoup(page_response.content, 'html.parser')

    pokedex = {}
    #i = 1
    pokemonRows = page_content.find_all('tr')
    for row in pokemonRows[1:]:
        
        statsHtml = row.find_all('td')[4:]
        statsArray = list(map(lambda data: int(data.text), statsHtml))

        typesHtml = row.find_all('a', attrs = {'class':'type-icon'})
        typesArray = list(map(lambda data: TYPES[str(data.text).upper()], typesHtml))

        name = row.find('a', attrs = {'class':'ent-name'}).text

        megaHtml = row.find('small', attrs = {'class':'text-muted'})
        if megaHtml:
            name = megaHtml.text
        
        pokedex[str(name)] = {
            NAME: str(name),
            TYPE1: typesArray[0]
        }

        if len(typesArray) > 1:
            pokedex[str(name)][TYPE2] = typesArray[1]
        
        pokedex[str(name)][HP] = statsArray[0]
        pokedex[str(name)][ATTACK] = statsArray[1]
        pokedex[str(name)][DEFENSE] = statsArray[2]
        pokedex[str(name)][SPATTACK] = statsArray[3]
        pokedex[str(name)][SPDEFENSE] = statsArray[4]
        pokedex[str(name)][SPEED] = statsArray[5]

        # ev_yield = get_pokemon_ev_yield(i, page_content2)
        # pokedex[str(name)][BASE_EXP] = ev_yield[str(name)][BASE_EXP] 
        # pokedex[str(name)][HP_YIELD] = ev_yield[str(name)][HP_YIELD] 
        # pokedex[str(name)][ATTACK_YIELD] = ev_yield[str(name)][ATTACK_YIELD] 
        # pokedex[str(name)][DEFENSE_YIELD] = ev_yield[str(name)][DEFENSE_YIELD] 
        # pokedex[str(name)][SPATTACK_YIELD] = ev_yield[str(name)][SPATTACK_YIELD] 
        # pokedex[str(name)][SPDEFENSE_YIELD] = ev_yield[str(name)][SPDEFENSE_YIELD] 
        # pokedex[str(name)][SPEED_YIELD] = ev_yield[str(name)][SPEED_YIELD] 
        # i += 1

    #D:/Documents/Python-Projects/
    with open('D:/Documents/Python-Projects/Game/database/pokedex.json', 'w') as outfile:
        dump(pokedex, outfile)

def get_pokemon_ev_yield():
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_effort_value_yield'
    
    try:
        page_response = get(url, timeout = 5)
    except Exception:
        print('No hay conexión de internet')
        return None

    page_content = BeautifulSoup(page_response.content, 'html.parser')

    ev_yield = {}

    pokemonRows = page_content.find_all('tr')
    for row in pokemonRows[1:1004]:
        
        statsHtml = row.find_all('td')[3:10]
        statsArray = list(map(lambda data: int(data.text), statsHtml))

        name = row.find('a')
        name = str(name)[15 : str(name).find('_')]

        megaHtml = row.find('small')
        if megaHtml:
            name = str(megaHtml.text)[1 : len(str(megaHtml.text)) -1 ]
        
        ev_yield[str(name)] = {
            NAME: str(name),
            BASE_EXP: statsArray[0],
            HP_YIELD: statsArray[1],
            ATTACK_YIELD: statsArray[2],
            DEFENSE_YIELD: statsArray[3],
            SPATTACK_YIELD:statsArray[4],
            SPDEFENSE_YIELD: statsArray[5],
            SPEED_YIELD: statsArray[6]        
        }


    #return ev_yield
    #D:/Documents/Python-Projects/
    with open('D:/Documents/Python-Projects/Game/database/baseExp_EV.json', 'w') as outfile:
        dump(ev_yield, outfile)

def get_pokemon_attacks():
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_moves'

    try:
        page_response = get(url, timeout = 5)
    except Exception:
        print('No hay conexión de internet')
        return None

    page_content = BeautifulSoup(page_response.content, 'html.parser')

    attacks = {}
    i = 0
    pokemonRows = page_content.find_all('tr')
    for row in pokemonRows[2:828]:
        
        statsHtml = row.find_all('td')
        attacksArray = list(map(lambda data: data.text, statsHtml))

        name = str(attacksArray[1]).replace("*", " ").rstrip().upper()        
        type = str(attacksArray[2]).replace("*", " ").rstrip().upper()        
        category = str(attacksArray[3]).replace("*", " ").rstrip().upper()        
        pp = str(attacksArray[5]).replace("*", " ").rstrip().upper()        
        power = str(attacksArray[6]).replace("*", " ").rstrip().upper()
        if power.find('—') == 0:
            power = 0

        accuracy = str(attacksArray[7]).replace("*", " ").rstrip().upper()        
        accuracy = accuracy.replace("%", " ")
        accuracy = accuracy.replace("*", " ")
        if accuracy.find('—') == 0:
            accuracy = 0

        #attacks[int(i)] = {
        attacks[name] = {            
            NAME: name,
            TYPE: type,
            CATEGORY: category,
            POWER: power,
            ACCURACY: accuracy,
            PP: pp
        }
        i += 1        

    with open('D:/Documents/Python-Projects/Game/database/attacks.json', 'w') as outfile:
        dump(attacks, outfile)


def get_evolution_list():
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_evolution_family'

    try:
        page_response = get(url, timeout = 5)
    except Exception:
        print('No hay conexión de internet')
        return None

    page_content = BeautifulSoup(page_response.content, 'html.parser')

    evolutions = {}
    i = 0
    pokemonRows = page_content.find_all('tr')
    for row in pokemonRows[:1040]:
        evoHtml = row.find_all('td')
        evolutionArray = list(map(lambda data: data.text, evoHtml))     
        if len(evolutionArray) == 0:
            continue

        if len(evolutionArray) > 0:
            if evolutionArray[0] == '\n':
                first_pokemon = str(evolutionArray[1]).rstrip()
                if len(evolutionArray) > 3 and evolutionArray[3] != '\xa0\n':
                    evo = str(evolutionArray[2]).rstrip()
                    second_pokemon = str(evolutionArray[4]).rstrip()
                else:
                    length = 0        

        if len(evolutionArray) == 8 and evolutionArray[0] == '\n':             
            length = 8
            #print(str(evolutionArray[1]).rstrip(), str(evolutionArray[2]).rstrip(), str(evolutionArray[4]).rstrip(), str(evolutionArray[5]).rstrip(), str(evolutionArray[7]).rstrip())

            if 'Unown' in [str(evolutionArray[1]).rstrip()[0:5], str(evolutionArray[4]).rstrip()[0:5], str(evolutionArray[7]).rstrip()[0:5]]:
                evolutions[str(evolutionArray[1]).rstrip()] = {
                    NAME: str(evolutionArray[1]).rstrip(),
                    'CONDITION': None,
                    'EVOLUTION': None
                }   

                evolutions[str(evolutionArray[4]).rstrip()] = {
                    NAME: str(evolutionArray[4]).rstrip(),
                    'CONDITION': None,
                    'EVOLUTION': None
                }   

                evolutions[str(evolutionArray[7]).rstrip()] = {
                    NAME: str(evolutionArray[7]).rstrip(),
                    'CONDITION': None,
                    'EVOLUTION': None
                }                                   
                continue

            if any(map(str.isdigit, str(evolutionArray[2]))):
                detonator = str(evolutionArray[2]).rstrip().replace('Level', ' ')
                detonator = detonator.replace('→', ' ')
                detonator = detonator.strip()
            else:
                detonator = str(evolutionArray[2]).replace('→', ' ').rstrip()

            name = str(evolutionArray[1]).replace('\u2640', ' (female)').rstrip()
            name = name.replace('\u2642', ' (male)').rstrip()
            name = name.replace('\u00e9', 'e')
            evolutions[name] = {
                NAME: name,
                'CONDITION': detonator.replace('\u00e9', 'e'),
                'EVOLUTION': str(evolutionArray[4]).rstrip()
            }

            if any(map(str.isdigit, str(evolutionArray[5]))):
                detonator = str(evolutionArray[5]).rstrip().replace('Level', ' ')
                detonator = detonator.replace('→', ' ')
                detonator = detonator.strip()
            else:
                detonator = str(evolutionArray[5]).replace('→', ' ').rstrip()

            name = str(evolutionArray[4]).replace('\u00e9', 'e').rstrip()
            evolutions[str(evolutionArray[4]).rstrip()] = {
                NAME: name,
                'CONDITION': detonator.replace('\u00e9', 'e'),
                'EVOLUTION': str(evolutionArray[7]).rstrip()
            }            
            continue

        if len(evolutionArray) in [5] and evolutionArray[0] == '\n':     
            length = 6
            #print(str(evolutionArray[1]).rstrip(), str(evolutionArray[2]).rstrip(), str(evolutionArray[4]).rstrip()) 

            if any(map(str.isdigit, str(evolutionArray[2]))):
                detonator = str(evolutionArray[2]).rstrip().replace('Level', ' ')
                detonator = detonator.replace('→', ' ')
                detonator = detonator.strip()
            else:
                detonator = str(evolutionArray[2]).replace('→', ' ').rstrip()

            name = str(evolutionArray[1]).replace('\u00e9', 'e').rstrip()
            evolutions[name] = {
                NAME: name,
                'CONDITION': detonator.replace('\u00e9', 'e'),
                'EVOLUTION': str(evolutionArray[4]).rstrip()
            }         
            continue

        if len(evolutionArray) in [6] and evolutionArray[0] == '\n':     
            length = 6
            #print(str(evolutionArray[1]).rstrip(), str(evolutionArray[2]).rstrip(), str(evolutionArray[4]).rstrip(), str(evolutionArray[5]).rstrip()) 

            if 'Unown' in [str(evolutionArray[1]).rstrip()[0:5], str(evolutionArray[4]).rstrip()[0:5]]:
                evolutions[str(evolutionArray[1]).rstrip()] = {
                    NAME: str(evolutionArray[1]).rstrip(),
                    'CONDITION': None,
                    'EVOLUTION': None
                }   

                evolutions[str(evolutionArray[4]).rstrip()] = {
                    NAME: str(evolutionArray[4]).rstrip(),
                    'CONDITION': None,
                    'EVOLUTION': None
                }                                 
                continue

            if any(map(str.isdigit, str(evolutionArray[2]))):
                detonator = str(evolutionArray[2]).rstrip().replace('Level', ' ')
                detonator = detonator.replace('→', ' ')
                detonator = detonator.strip()
            else:
                detonator = str(evolutionArray[2]).replace('→', ' ').rstrip()

            name = str(evolutionArray[1]).replace('\u00e9', 'e').rstrip()
            evolutions[name] = {
                NAME: name,
                'CONDITION': detonator.replace('\u00e9', 'e'),
                'EVOLUTION': str(evolutionArray[4]).rstrip() + str(evolutionArray[5]).rstrip()
            }        
            continue

        if len(evolutionArray) in [3, 4]:        
            if length == 8:
                #print(first_pokemon, evo, second_pokemon, str(evolutionArray[0]).rstrip(), str(evolutionArray[2]).rstrip())

                if any(map(str.isdigit, evo)):
                    detonator = evo.replace('Level', ' ')
                    detonator = detonator.replace('→', ' ')
                    detonator = detonator.strip()
                else:
                    detonator = evo.replace('→', ' ')

                first_pokemon = first_pokemon.replace('\u00e9', 'e').rstrip()  
                evolutions[first_pokemon] = {
                    NAME: first_pokemon,
                    'CONDITION': detonator.replace('\u00e9', 'e'),
                    'EVOLUTION': second_pokemon
                }   

                if any(map(str.isdigit, str(evolutionArray[0]))):
                    detonator = str(evolutionArray[0]).rstrip().replace('Level', ' ')
                    detonator = detonator.replace('→', ' ')
                    detonator = detonator.strip()
                else:
                    detonator = str(evolutionArray[0]).replace('→', ' ').rstrip()
                
                second_pokemon = second_pokemon.replace('\u00e9', 'e').rstrip()  
                evolutions[second_pokemon] = {
                    NAME: second_pokemon,
                    'CONDITION': detonator.replace('\u00e9', 'e'),
                    'EVOLUTION': str(evolutionArray[2]).rstrip()
                }                                    
                length = 0
                continue
            elif length == 6 or len(evolutionArray) == 4:
                #print(first_pokemon, str(evolutionArray[0]).rstrip(), str(evolutionArray[2]).rstrip()) 
                if any(map(str.isdigit, str(evolutionArray[0]))):
                    detonator = str(evolutionArray[0]).rstrip().replace('Level', ' ')
                    detonator = detonator.replace('→', ' ')
                    detonator = detonator.strip()
                else:
                    detonator = str(evolutionArray[0]).replace('→', ' ').rstrip()

                first_pokemon = first_pokemon.replace('\u00e9', 'e').rstrip()  
                evolutions[first_pokemon] = {
                    NAME: first_pokemon,
                    'CONDITION': detonator.replace('\u00e9', 'e'),
                    'EVOLUTION': str(evolutionArray[2]).rstrip()
                }                    
                length = 0   
                continue
            elif length == 0:
                #print(str(evolutionArray[1]).rstrip())       
                name = str(evolutionArray[1]).replace('\u00e9', 'e').rstrip()                    
                evolutions[name] = {
                    NAME: name,
                    'CONDITION': None,
                    'EVOLUTION': None
                }                 
                length = 0  
                continue

        if len(evolutionArray) == 6:
            #print(first_pokemon, str(evolutionArray[0]).rstrip(), str(evolutionArray[2]).rstrip(), str(evolutionArray[3]).rstrip(), str(evolutionArray[5]).rstrip())  
            if first_pokemon == "Mime Jr.":
                first_pokemon += " (Galar)"
            if first_pokemon == "Wurmple":
                first_pokemon += "+"

            if any(map(str.isdigit, str(evolutionArray[0]))):
                detonator = str(evolutionArray[0]).rstrip().replace('Level', ' ')
                detonator = detonator.replace('→', ' ')
                detonator = detonator.strip()
            else:
                detonator = str(evolutionArray[0]).replace('→', ' ').rstrip()

            first_pokemon = first_pokemon.replace('\u00e9', 'e').rstrip()       
            evolutions[first_pokemon] = {
                NAME: first_pokemon,
                'CONDITION' : detonator.replace('\u00e9', 'e'),
                'EVOLUTION' : str(evolutionArray[2]).rstrip()
            }

            if any(map(str.isdigit, str(evolutionArray[3]))):
                detonator = str(evolutionArray[3]).rstrip().replace('Level', ' ')
                detonator = detonator.replace('→', ' ')
                detonator = detonator.strip()
            else:
                detonator = str(evolutionArray[3]).replace('→', ' ').rstrip()

            name = str(evolutionArray[2]).replace('\u00e9', 'e').rstrip()  
            evolutions[name] = {
                NAME: name,
                'CONDITION': detonator.replace('\u00e9', 'e'),
                'EVOLUTION': str(evolutionArray[5]).rstrip()
            }                                         
    #D:/Documents/Python-Projects/
    with open('Game/database/evolutions.json', 'w') as outfile:
        dump(evolutions, outfile)

def get_pokemon_ability():
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_Ability'

    try:
        page_response = get(url, timeout = 5)
    except Exception:
        print('No hay conexión de internet')
        return None

    page_content = BeautifulSoup(page_response.content, 'html.parser')

    abilities = {}
    i = 0
    pokemonRows = page_content.find_all('tr')
    for row in pokemonRows:
        
        statsHtml = row.find_all('td')
        abilitiesArray = list(map(lambda data: data.text, statsHtml))
        
        if len(abilitiesArray) == 6:
            name = str(abilitiesArray[2]).replace("*", " ").rstrip()
            if name.find('(') > 0:
                begin = int(name.find('(')) + 1
                end = int(name.find(')'))
                name = str((abilitiesArray[2])[begin:end]).replace("*", " ").rstrip()
                
            ability1 = str(abilitiesArray[3]).replace("*", " ").rstrip().upper()
            ability2 = str(abilitiesArray[4]).replace("*", " ").rstrip().upper()
            hidden = str(abilitiesArray[5]).replace("*", " ").rstrip().upper()
        else:
            continue

        abilities[name] = {            
            NAME: name,
            FIRST: ability1,
            SECOND: ability2,
            HIDDEN: hidden
        }
        i += 1        

    with open(path_abilities, 'w') as outfile:
        dump(abilities, outfile)

def get_item_gen5():
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_V)'

    try:
        page_response = get(url, timeout = 5)
    except Exception:
        print('No hay conexión de internet')
        return None

    page_content = BeautifulSoup(page_response.content, 'html.parser')

    items = {}
    tableRows = page_content.find_all('tr')
    for row in tableRows[3:643]:
        statsHtml = row.find_all('td')
        itemsArray = list(map(lambda data: data.text, statsHtml))

        itemno = str(itemsArray[0]).rstrip()
        item = str(itemsArray[3]).rstrip().replace('*', ' ')
        pocket = str(itemsArray[5]).rstrip()

        if pocket == 'Unknown pocket':
            continue
        
        if pocket == 'Poké Balls pocket':
            items[item] = {            
                'CODE': itemno,
                NAME: item,
                'POCKET': ITEMS,
                TYPE: 0
            }
            continue

        if pocket == 'Items pocket':
            items[item] = {            
                'CODE': itemno,
                NAME: item,
                'POCKET': ITEMS,
                TYPE: 1
            }
            continue

        if pocket == 'Medicine pocket':
            items[item] = {            
                'CODE': itemno,
                NAME: item,
                'POCKET': MEDICINE,
                TYPE: 2
            }
            continue

        if pocket == 'TMs and HMs pocket':
            items[item] = {            
                'CODE': itemno,
                NAME: item,
                'POCKET': TM_HM,
                TYPE: 3
            }
            continue  

        if pocket == 'Berries pocket': 
            items[item] = {            
                'CODE': itemno,
                NAME: item,
                'POCKET': BERRIES,
                TYPE: 4
            }
            continue

        if pocket == 'Key items pocket':
            items[item] = {            
                'CODE': itemno,
                NAME: item,
                'POCKET': KEY_ITEMS,
                TYPE: 5
            }
            continue              

    with open(path_items, 'w') as outfile:
        dump(items, outfile)

# get_pokedex()
# get_pokemon_ev_yield()
# get_pokemon_attacks()
# get_evolution_list()
# get_pokemon_ability()
get_item_gen5()