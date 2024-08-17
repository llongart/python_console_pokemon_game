from os import path 

# Global variables
is_critical_attack = False
type_effectiveness = 1
db_pokemon_list = None
db_base_ev_list = None
db_attack_list = None
db_abilities = None
db_learnsets = None
db_savegame = None
is_evolving = False
path_evolutions = path.join(path.dirname(__file__), 'database\\evolutions.json')
path_savegame = path.join(path.dirname(__file__), 'database\\savegame.json')
path_attacks = path.join(path.dirname(__file__), 'database\\attacks.json')
path_pokedex = path.join(path.dirname(__file__), 'database\\pokedex.json')
path_base_ev = path.join(path.dirname(__file__), 'database\\baseExp_EV.json')
path_abilities = path.join(path.dirname(__file__), 'database\\abilities.json')
path_learnsets = path.join(path.dirname(__file__), 'database\\learnsets.json')
path_items = path.join(path.dirname(__file__), 'database\\items.json')
applied = False

# Trainers
PLAYER = 'PLAYER'
TRAINER = 'TRAINER'
RIVAL = 'RIVAL'
TYPE1 = 'TYPE1'
TYPE2 = 'TYPE2'
GENDER = 'GENDER'
MONEY = 'MONEY'
BAG = 'BAG'
ITEMS = 'ITEMS'
MEDICINE = 'MEDICINE'
TM_HM = 'TM_HM'
BERRIES = 'BERRIES'
KEY_ITEMS = 'KEY_ITEMS'
FREE_SPACE = 'FREE_SPACE'
POKEMONS = 'POKEMONS'
BADGES = 'BADGES'
BADGE1 = 'BADGE1'
BADGE2 = 'BADGE2'
BADGE3 = 'BADGE3'
BADGE4 = 'BADGE4'
BADGE5 = 'BADGE5'
BADGE6 = 'BADGE6'
BADGE7 = 'BADGE7'
BADGE8 = 'BADGE8'

#ITEMS
QUANTITY = 'QUANTITY'

# BADGES
TRAINER_BADGES = {
    BADGE1: 0,
    BADGE2: 0,
    BADGE3: 0,
    BADGE4: 0,
    BADGE5: 0,
    BADGE6: 0,
    BADGE7: 0,
    BADGE8: 0
}

# POKEMON
LEVEL = 'LEVEL'
CURRENT_STATUS = 'CURRENT_STATUS'
ATTACKS = 'ATTACKS'
STATS = 'STATS'
BASE_STATS = 'BASE_STATS'
IV = 'IV'
EV = 'EV'
EVASION = 'EVASION'
NATURE_VAL = 'NATURE'
NATURE_TYPE = 'NATURE_TYPE'
ABILITY = 'ABILITY'
BASE_EXP = 'BASE_EXP'
GROWNING_TYPE_VAL = 'GROWNING_TYPE'
CURRENT_EXP = 'CURRENT_EXP'
EXP_NEXT_LEVEL = 'EXP_NEXT_LEVEL'
CURRENT_HP = 'CURRENT_HP'
EVOLUTION = 'EVOLUTION'
MASTER = 'MASTER'
HELD = 'HELD'
FRIENDSHIP = 'FRIENDSHIP'
CATCH_RATE = 'CATCH_RATE'

# Pokemon growning types
ERRATIC = 'ERRATIC'
FAST = 'FAST'
MEDIUM_FAST = 'MEDIUM_FAST'
MEDIUM_SLOW = 'MEDIUM_SLOW'
SLOW = 'SLOW'
FLUCTUATING = 'FLUCTUATING'

GROWNING_TYPE = {
    0 : ERRATIC,
    1 : FAST,
    2 : MEDIUM_FAST,
    3 : MEDIUM_SLOW,
    4 : SLOW,
    5 : FLUCTUATING
}

# Pokemon STATS
HP = 'HP'
ATTACK = 'ATTACK'
DEFENSE = 'DEFENSE'
SPATTACK = 'SPATTACK'
SPDEFENSE = 'SPDEFENSE'
SPEED = 'SPEED'

BASE_EXP = 'BASE_EXP'

HP_YIELD = 'HP_YIELD'
ATTACK_YIELD = 'ATTACK_YIELD'
DEFENSE_YIELD = 'DEFENSE_YIELD'
SPATTACK_YIELD = 'SPATTACK_YIELD'
SPDEFENSE_YIELD = 'SPDEFENSE_YIELD'
SPEED_YIELD = 'SPEED_YIELD'

# Pokemon abilities
FIRST = 'FIRST_ABILITY'
SECOND = 'SECOND_ABILITY'
HIDDEN = 'HIDDEN_ABILITY'

# Attack structure
NAME = 'NAME'
TYPE = 'TYPE'
CATEGORY = 'CATEGORY'
POWER = 'POWER'
PP = 'PP'
ACCURACY = 'ACCURACY'

# Attack categories
PHYSICAL = 'PHYSICAL'
SPECIAL = 'SPECIAL'
STATUS = 'STATUS'

# Attack stages
STAGE_0 = 1 / 24
STAGE_1 = 0.125
STAGE_2 = 0.5
STAGE_3 = 1

# Pokemon STATUS
ST_NORMAL = 'NORMAL'
ST_BURNED = 'BURNED'
ST_FREEZED = 'FREEZED'
ST_PARALYZED = 'PARALYZED'
ST_POISONED = 'POISONED'
ST_BADLYPOISON = 'BADLY_POISONED'
ST_SLEEP = 'SLEEPED'
ST_BOUND = 'BOUNDED'
ST_CONFUSION = 'CONFUSED'
ST_CANT_ESCAPE = 'CANT_ESCAPE'
ST_FAINTED = 'FAINTED'
# THERE'S MORE

# Attack stat by category
ATTACK_STAT = {
    PHYSICAL: ATTACK,
    SPECIAL: SPATTACK
}

# Defense stat by category
DEFENSE_STAT = {
    PHYSICAL: DEFENSE,
    SPECIAL: SPDEFENSE
}

STAT_STAGE_MULTIPLIER = {
    -6: 2/8,
    -5: 2/7,
    -4: 2/6,
    -3: 2/5,
    -2: 2/4,
    -1: 2/3,
     0: 2/2,
     1: 3/2,
     2: 4/2,
     3: 5/2,
     4: 6/2,
     5: 7/2,
     6: 8/2
}

ACCURACY_STAGE_MULTIPLIER = {
    -6: 3/9,
    -5: 3/8,
    -4: 3/7,
    -3: 3/6,
    -2: 3/5,
    -1: 3/4,
     0: 3/3,
     1: 4/3,
     2: 5/3,
     3: 6/3,
     4: 7/3,
     5: 8/3,
     6: 9/3
}

EVASION_STAGE_MULTIPLIER = {
    -6: 9/3,
    -5: 8/3,
    -4: 7/3,
    -3: 6/3,
    -2: 5/3,
    -1: 4/3,
     0: 3/3,
     1: 3/4,
     2: 3/5,
     3: 3/6,
     4: 3/7,
     5: 3/8,
     6: 3/9,
}

# Pokemon/Attack types
BUG = 'BUG'
DRAGON = 'DRAGON'
DARK = 'DARK'
ELECTRIC = 'ELECTRIC'
FIRE = 'FIRE'
FIGHTING = 'FIGHTING'
FLYING = 'FLYING'
FAIRY = 'FAIRY'
GROUND = 'GROUND'
GHOST = 'GHOST'
GRASS = 'GRASS'
ICE = 'ICE'
NORMAL = 'NORMAL'
PSYCHIC = 'PSYCHIC'
POISON = 'POISON' 
ROCK = 'ROCK'
STEEL = 'STEEL'
WATER = 'WATER'

TYPES = {
    BUG : 'BUG',
    DRAGON : 'DRAGON',
    DARK : 'DARK',
    ELECTRIC : 'ELECTRIC',
    FIRE : 'FIRE',
    FIGHTING : 'FIGHTING',
    FLYING : 'FLYING',
    FAIRY : 'FAIRY',
    GROUND : 'GROUND',
    GHOST : 'GHOST',
    GRASS : 'GRASS',
    ICE : 'ICE',
    NORMAL : 'NORMAL',
    PSYCHIC : 'PSYCHIC',
    POISON : 'POISON', 
    ROCK : 'ROCK',
    STEEL : 'STEEL',
    WATER : 'WATER',
}
# Commands
FIGHT = 'FIGHT'
BAG = 'BAG'
POKEMON = 'POKEMON'
FLEE = 'FLEE'

# Type effectiveness
W = 0.5 # W = Weak defense (0.5x)
N = 1   # N = Neutral defense (1x)
R = 2   # R = Resistant defense (2x)
I = 0   # I = Inmune (0x)

# Defending effectiveness
DEFENSE_EFFECTIVENESS = {
    NORMAL:   { NORMAL: N, FIGHTING: R, FLYING: N, POISON: N, GROUND: N, ROCK: N, BUG: N, GHOST: I, STEEL: N, FIRE: N, WATER: N, GRASS: N, ELECTRIC: N, PSYCHIC: N, ICE: N, DRAGON: N, DARK: N, FAIRY: N },
    FIGHTING: { NORMAL: N, FIGHTING: N, FLYING: R, POISON: N, GROUND: N, ROCK: W, BUG: W, GHOST: N, STEEL: N, FIRE: N, WATER: N, GRASS: N, ELECTRIC: N, PSYCHIC: R, ICE: N, DRAGON: N, DARK: W, FAIRY: R },
    FLYING:   { NORMAL: N, FIGHTING: W, FLYING: N, POISON: N, GROUND: I, ROCK: R, BUG: W, GHOST: N, STEEL: N, FIRE: N, WATER: N, GRASS: W, ELECTRIC: R, PSYCHIC: N, ICE: R, DRAGON: N, DARK: N, FAIRY: N },
    POISON:   { NORMAL: N, FIGHTING: W, FLYING: N, POISON: W, GROUND: R, ROCK: N, BUG: W, GHOST: N, STEEL: N, FIRE: N, WATER: N, GRASS: W, ELECTRIC: N, PSYCHIC: R, ICE: N, DRAGON: N, DARK: N, FAIRY: W },
    GROUND:   { NORMAL: N, FIGHTING: N, FLYING: N, POISON: W, GROUND: N, ROCK: W, BUG: N, GHOST: N, STEEL: N, FIRE: N, WATER: R, GRASS: R, ELECTRIC: I, PSYCHIC: N, ICE: R, DRAGON: N, DARK: N, FAIRY: N },
    ROCK:     { NORMAL: W, FIGHTING: R, FLYING: W, POISON: W, GROUND: R, ROCK: N, BUG: N, GHOST: N, STEEL: R, FIRE: W, WATER: R, GRASS: R, ELECTRIC: N, PSYCHIC: N, ICE: N, DRAGON: N, DARK: N, FAIRY: N },
    BUG:      { NORMAL: N, FIGHTING: W, FLYING: R, POISON: N, GROUND: W, ROCK: R, BUG: N, GHOST: N, STEEL: N, FIRE: R, WATER: N, GRASS: W, ELECTRIC: N, PSYCHIC: N, ICE: N, DRAGON: N, DARK: N, FAIRY: N },
    GHOST:    { NORMAL: I, FIGHTING: I, FLYING: N, POISON: W, GROUND: N, ROCK: N, BUG: W, GHOST: R, STEEL: N, FIRE: N, WATER: N, GRASS: N, ELECTRIC: N, PSYCHIC: N, ICE: N, DRAGON: N, DARK: R, FAIRY: N },
    STEEL:    { NORMAL: W, FIGHTING: R, FLYING: W, POISON: I, GROUND: R, ROCK: W, BUG: W, GHOST: N, STEEL: W, FIRE: R, WATER: N, GRASS: W, ELECTRIC: N, PSYCHIC: W, ICE: W, DRAGON: W, DARK: N, FAIRY: W },
    FIRE:     { NORMAL: N, FIGHTING: N, FLYING: N, POISON: N, GROUND: R, ROCK: R, BUG: W, GHOST: N, STEEL: W, FIRE: W, WATER: R, GRASS: W, ELECTRIC: N, PSYCHIC: N, ICE: W, DRAGON: N, DARK: N, FAIRY: W },
    WATER:    { NORMAL: N, FIGHTING: N, FLYING: N, POISON: N, GROUND: N, ROCK: N, BUG: N, GHOST: N, STEEL: W, FIRE: W, WATER: W, GRASS: R, ELECTRIC: R, PSYCHIC: N, ICE: W, DRAGON: N, DARK: N, FAIRY: N },
    GRASS:    { NORMAL: N, FIGHTING: N, FLYING: R, POISON: R, GROUND: W, ROCK: N, BUG: R, GHOST: N, STEEL: N, FIRE: R, WATER: W, GRASS: W, ELECTRIC: W, PSYCHIC: N, ICE: R, DRAGON: N, DARK: N, FAIRY: N },
    ELECTRIC: { NORMAL: N, FIGHTING: N, FLYING: W, POISON: N, GROUND: R, ROCK: N, BUG: N, GHOST: N, STEEL: W, FIRE: N, WATER: N, GRASS: N, ELECTRIC: W, PSYCHIC: N, ICE: N, DRAGON: N, DARK: N, FAIRY: N },
    PSYCHIC:  { NORMAL: N, FIGHTING: W, FLYING: N, POISON: N, GROUND: N, ROCK: N, BUG: R, GHOST: R, STEEL: N, FIRE: N, WATER: N, GRASS: N, ELECTRIC: N, PSYCHIC: W, ICE: N, DRAGON: N, DARK: R, FAIRY: N },
    ICE:      { NORMAL: N, FIGHTING: R, FLYING: N, POISON: N, GROUND: N, ROCK: R, BUG: N, GHOST: N, STEEL: R, FIRE: R, WATER: N, GRASS: N, ELECTRIC: N, PSYCHIC: N, ICE: W, DRAGON: N, DARK: N, FAIRY: N },
    DRAGON:   { NORMAL: N, FIGHTING: N, FLYING: N, POISON: N, GROUND: N, ROCK: N, BUG: N, GHOST: N, STEEL: N, FIRE: W, WATER: W, GRASS: W, ELECTRIC: W, PSYCHIC: N, ICE: R, DRAGON: R, DARK: N, FAIRY: R },
    DARK:     { NORMAL: N, FIGHTING: R, FLYING: N, POISON: N, GROUND: N, ROCK: N, BUG: R, GHOST: W, STEEL: N, FIRE: N, WATER: N, GRASS: N, ELECTRIC: N, PSYCHIC: I, ICE: N, DRAGON: N, DARK: W, FAIRY: R },
    FAIRY:    { NORMAL: N, FIGHTING: W, FLYING: N, POISON: R, GROUND: N, ROCK: N, BUG: W, GHOST: N, STEEL: R, FIRE: N, WATER: N, GRASS: N, ELECTRIC: N, PSYCHIC: N, ICE: N, DRAGON: I, DARK: W, FAIRY: N }
}
 
# Natures
HARDY = 'HARDY'
BOLD = 'BOLD'
MODEST = 'MODEST'
CALM = 'CALM'
TIMID = 'TIMID'
LONELY = 'LONELY'
DOCILE = 'DOCILE'
MILD = 'MILD'
GENTLE = 'GENTLE'
HASTY = 'HASTY'
ADAMANT = 'ADAMANT'
IMPISH = 'IMPISH'
BASHFUL = 'BASHFUL'
CAREFUL = 'CAREFUL'
JOLLY = 'JOLLY'
NAUGHTY = 'NAUGHTY'
LAX = 'LAX'
RASH = 'RASH'
QUIRKY = 'QUIRKY'
NAIVE = 'NAIVE'
BRAVE = 'BRAVE'
RELAXED = 'RELAXED'
QUIET = 'QUIET'
SASSY = 'SASSY'
SERIOUS = 'SERIOUS'

# Type natures
D = 0.9 # Down stat nature
U = 1.1 # Up stat nature

NATURE = {
    HARDY:   { ATTACK: N, DEFENSE: N, SPATTACK: N, SPDEFENSE: N, SPEED: N },
    BOLD:    { ATTACK: D, DEFENSE: U, SPATTACK: N, SPDEFENSE: N, SPEED: N },
    MODEST:  { ATTACK: D, DEFENSE: N, SPATTACK: U, SPDEFENSE: N, SPEED: N },
    CALM:    { ATTACK: D, DEFENSE: N, SPATTACK: N, SPDEFENSE: U, SPEED: N },
    TIMID:   { ATTACK: D, DEFENSE: N, SPATTACK: N, SPDEFENSE: N, SPEED: U },

    LONELY:  { ATTACK: U, DEFENSE: D, SPATTACK: N, SPDEFENSE: N, SPEED: N },
    DOCILE:  { ATTACK: N, DEFENSE: N, SPATTACK: N, SPDEFENSE: N, SPEED: N },
    MILD:    { ATTACK: N, DEFENSE: D, SPATTACK: U, SPDEFENSE: N, SPEED: N },
    GENTLE:  { ATTACK: N, DEFENSE: D, SPATTACK: N, SPDEFENSE: U, SPEED: N },
    HASTY:   { ATTACK: N, DEFENSE: D, SPATTACK: N, SPDEFENSE: N, SPEED: U },

    ADAMANT: { ATTACK: U, DEFENSE: N, SPATTACK: D, SPDEFENSE: N, SPEED: N },
    IMPISH:  { ATTACK: N, DEFENSE: U, SPATTACK: D, SPDEFENSE: N, SPEED: N },
    BASHFUL: { ATTACK: N, DEFENSE: N, SPATTACK: N, SPDEFENSE: N, SPEED: N },
    CAREFUL: { ATTACK: N, DEFENSE: N, SPATTACK: D, SPDEFENSE: U, SPEED: N },
    JOLLY:   { ATTACK: N, DEFENSE: N, SPATTACK: D, SPDEFENSE: N, SPEED: U },

    NAUGHTY: { ATTACK: U, DEFENSE: N, SPATTACK: N, SPDEFENSE: D, SPEED: N },
    LAX:     { ATTACK: N, DEFENSE: U, SPATTACK: N, SPDEFENSE: D, SPEED: N },
    RASH:    { ATTACK: N, DEFENSE: N, SPATTACK: U, SPDEFENSE: D, SPEED: N },
    QUIRKY:  { ATTACK: N, DEFENSE: N, SPATTACK: N, SPDEFENSE: N, SPEED: N },
    NAIVE:   { ATTACK: N, DEFENSE: N, SPATTACK: N, SPDEFENSE: D, SPEED: U },

    BRAVE:   { ATTACK: U, DEFENSE: N, SPATTACK: N, SPDEFENSE: N, SPEED: D },
    RELAXED: { ATTACK: N, DEFENSE: U, SPATTACK: N, SPDEFENSE: N, SPEED: D },
    QUIET:   { ATTACK: N, DEFENSE: N, SPATTACK: U, SPDEFENSE: N, SPEED: D },
    SASSY:   { ATTACK: N, DEFENSE: N, SPATTACK: N, SPDEFENSE: U, SPEED: D },
    SERIOUS: { ATTACK: N, DEFENSE: N, SPATTACK: N, SPDEFENSE: N, SPEED: D },    
}

# CPU IA
atk_count = 0
sta_count = 0
max_curation_usage = 0

# Semi-invulnerable moves
SEMI_INVULNERABLE_MOVES = (
    'BOUNCE',
    'DIG',
    'DIVE',
    'FLY',
    'PHANTOM FORCE',
    'SHADOW FORCE',
    'SKY DROP'
)

# Sound-based moves
SOUND_BASED_MOVES = (
    'BOOMBURST',
    'BUG BUZZ',
    'CHATTER',
    'CLANGING SCALES',
    'CLANGOROUS SOUL',
    'CLANGOROUS SOULBLAZE',
    'CONFIDE',
    'DISARMING VOICE',
    'ECHOED VOICE',
    'EERIE SPELL',
    'GRASS WHISTLE',
    'GROWL',
    'HEAL BELL',
    'HOWL',
    'HYPER VOICE',
    'METAL SOUND',
    'NOBLE ROAR',
    'OVERDRIVE',
    'PARTING SHOT',
    'PERISH SONG',
    'RELIC SONG',
    'ROAR',
    'ROUND',
    'SCREECH',
    'SHADOW PANIC',
    'SING',
    'SNARL',
    'SNORE',
    'SPARKLING ARIA',
    'SUPERSONIC',
    'UPROAR'
)

CONTACT_MOVES = (
    "POUND",
    "KARATE CHOP",
    "DOUBLE SLAP",
    "COMET PUNCH",
    "MEGA PUNCH",
    "FIRE PUNCH",
    "ICE PUNCH",
    "THUNDER PUNCH",
    "SCRATCH",
    "VISE GRIP",
    "GUILLOTINE",
    "CUT",
    "WING ATTACK",
    "FLY",
    "BIND",
    "SLAM",
    "VINE WHIP",
    "STOMP",
    "DOUBLE KICK",
    "MEGA KICK",
    "JUMP KICK",
    "ROLLING KICK",
    "HEADBUTT",
    "HORN ATTACK",
    "FURY ATTACK",
    "HORN DRILL",
    "TACKLE",
    "BODY SLAM",
    "WRAP",
    "TAKE DOWN",
    "THRASH",
    "DOUBLE-EDGE",
    "BITE",
    "PECK",
    "DRILL PECK",
    "SUBMISSION",
    "LOW KICK",
    "COUNTER",
    "SEISMIC TOSS",
    "STRENGTH",
    "PETAL DANCE",
    "DIG",
    "QUICK ATTACK",
    "RAGE",
    "BIDE",
    "LICK",
    "WATERFALL",
    "CLAMP",
    "SKULL BASH",
    "CONSTRICT",
    "HIGH JUMP KICK",
    "LEECH LIFE",
    "DIZZY PUNCH",
    "CRABHAMMER",
    "FURY SWIPES",
    "HYPER FANG",
    "SUPER FANG",
    "SLASH",
    "STRUGGLE",
    "TRIPLE KICK",
    "THIEF",
    "FLAME WHEEL",
    "FLAIL",
    "REVERSAL",
    "MACH PUNCH",
    "FEINT ATTACK",
    "OUTRAGE",
    "ROLLOUT",
    "FALSE SWIPE",
    "SPARK",
    "FURY CUTTER",
    "STEEL WING",
    "RETURN",
    "FRUSTRATION",
    "DYNAMIC PUNCH",
    "MEGAHORN",
    "PURSUIT",
    "RAPID SPIN",
    "IRON TAIL",
    "METAL CLAW",
    "VITAL THROW",
    "CROSS CHOP",
    "CRUNCH",
    "EXTREME SPEED",
    "ROCK SMASH",
    "FAKE OUT",
    "FACADE",
    "FOCUS PUNCH",
    "SMELLING SALTS",
    "SUPERPOWER",
    "REVENGE",
    "BRICK BREAK",
    "KNOCK OFF",
    "ENDEAVOR",
    "DIVE",
    "ARM THRUST",
    "BLAZE KICK",
    "ICE BALL",
    "NEEDLE ARM",
    "POISON FANG",
    "CRUSH CLAW",
    "METEOR MASH",
    "ASTONISH",
    "SHADOW PUNCH",
    "SKY UPPERCUT",
    "AERIAL ACE",
    "DRAGON CLAW",
    "BOUNCE",
    "POISON TAIL",
    "COVET",
    "VOLT TACKLE",
    "LEAF BLADE",
    "WAKE-UP SLAP",
    "HAMMER ARM",
    "GYRO BALL",
    "PLUCK",
    "U-TURN",
    "CLOSE COMBAT",
    "PAYBACK",
    "ASSURANCE",
    "TRUMP CARD",
    "WRING OUT",
    "PUNISHMENT",
    "LAST RESORT",
    "SUCKER PUNCH",
    "FLARE BLITZ",
    "FORCE PALM",
    "POISON JAB",
    "NIGHT SLASH",
    "AQUA TAIL",
    "X-SCISSOR",
    "DRAGON RUSH",
    "DRAIN PUNCH",
    "BRAVE BIRD",
    "GIGA IMPACT",
    "BULLET PUNCH",
    "AVALANCHE",
    "SHADOW CLAW",
    "THUNDER FANG",
    "ICE FANG",
    "FIRE FANG",
    "SHADOW SNEAK",
    "ZEN HEADBUTT",
    "ROCK CLIMB",
    "POWER WHIP",
    "CROSS POISON",
    "IRON HEAD",
    "GRASS KNOT",
    "BUG BITE",
    "WOOD HAMMER",
    "AQUA JET",
    "HEAD SMASH",
    "DOUBLE HIT",
    "CRUSH GRIP",
    "SHADOW FORCE",
    "STORM THROW",
    "HEAVY SLAM",
    "FLAME CHARGE",
    "LOW SWEEP",
    "FOUL PLAY",
    "CHIP AWAY",
    "SKY DROP",
    "CIRCLE THROW",
    "ACROBATICS",
    "RETALIATE",
    "DRAGON TAIL",
    "WILD CHARGE",
    "DRILL RUN",
    "DUAL CHOP",
    "HEART STAMP",
    "HORN LEECH",
    "SACRED SWORD",
    "RAZOR SHELL",
    "HEAT CRASH",
    "STEAMROLLER",
    "TAIL SLAP",
    "HEAD CHARGE",
    "GEAR GRIND",
    "BOLT STRIKE",
    "V-CREATE",
    "FLYING PRESS",
    "FELL STINGER",
    "PHANTOM FORCE",
    "DRAINING KISS",
    "PLAY ROUGH",
    "NUZZLE",
    "HOLD BACK",
    "INFESTATION",
    "POWER-UP PUNCH",
    "DRAGON ASCENT",
    "CATASTROPIKA",
    "FIRST IMPRESSION",
    "DARKEST LARIAT",
    "ICE HAMMER",
    "HIGH HORSEPOWER",
    "SOLAR BLADE",
    "THROAT CHOP",
    "ANCHOR SHOT",
    "LUNGE",
    "FIRE LASH",
    "POWER TRIP",
    "SMART STRIKE",
    "TROP KICK",
    "DRAGON HAMMER",
    "BRUTAL SWING",
    "MALICIOUS MOONSAULT",
    "SOUL-STEALING 7-STAR STRIKE",
    "PULVERIZING PANCAKE",
    "PSYCHIC FANGS",
    "STOMPING TANTRUM",
    "ACCELEROCK",
    "LIQUIDATION",
    "SPECTRAL THIEF",
    "SUNSTEEL STRIKE",
    "ZING ZAP",
    "MULTI-ATTACK",
    "PLASMA FISTS",
    "SEARING SUNRAZE SMASH",
    "LET'S SNUGGLE FOREVER",
    "ZIPPY ZAP",
    "FLOATY FALL",
    "SIZZLY SLIDE",
    "VEEVEE VOLLEY",
    "DOUBLE IRON BASH",
    "JAW LOCK",
    "BOLT BEAK",
    "FISHIOUS REND",
    "BODY PRESS",
    "SNAP TRAP",
    "BEHEMOTH BLADE",
    "BEHEMOTH BASH",
    "BREAKING SWIPE",
    "BRANCH POKE",
    "SPIRIT BREAK",
    "FALSE SURRENDER",
    "STEEL ROLLER",
    "GRASSY GLIDE",
    "SKITTER SMACK",
    "LASH OUT",
    "FLIP TURN",
    "TRIPLE AXEL",
    "DUAL WINGBEAT",
    "WICKED BLOW",
    "SURGING STRIKES",
    "THUNDEROUS KICK"   
)

DAMAGE_REDUCING_BERRIES = (
    'Babiri Berry',
    'Charti Berry',
    'Chilan Berry',
    'Chople Berry',
    'Coba Berry',
    'Colbur Berry',
    'Haban Berry',
    'Kasib Berry',
    'Kebia Berry',
    'Occa Berry',
    'Passho Berry',
    'Payapa Berry',
    'Rindo Berry',
    'Roseli Berry',
    'Shuca Berry',
    'Tanga Berry',
    'Wacan Berry',
    'Yache Berry'
)


# BATTLE STAGES
WEATHER_TYPE = {
    0: "CLEAR SKIES",
    1: "HARSH SUNLIGHT",
    2: "EXTREMELY HARSH SUNLIGHT",
    3: "RAIN",
    4: "HEAVY RAIN",
    5: "SANDSTORM",
    6: "HAIL"
}

# POWER-UPS
is_set_atk1 = False
is_set_atk2 = False
is_set_spatk1 = False
is_set_spatk2 = False
is_set_speed1 = False
is_set_speed2 = False
is_set_spdef1 = False
is_set_spdef2 = False

# NATURAL GIFT BERRY USES
NATURAL_GIFT = {
    "Cheri Berry": { TYPE: FIRE, POWER: 60 },
    "Chesto Berry": { TYPE: WATER, POWER: 60 },
    "Pecha Berry": { TYPE: ELECTRIC, POWER: 60 },
    "Rawst Berry": { TYPE: GRASS, POWER: 60 },
    "Aspear Berry": { TYPE: ICE, POWER: 60 },
    "Leppa Berry": { TYPE: FIGHTING, POWER: 60 },
    "Oran Berry": { TYPE: POISON, POWER: 60 },
    "Persim Berry": { TYPE: GROUND, POWER: 60 },
    "Lum Berry": { TYPE: FLYING, POWER: 60 },
    "Sitrus Berry": { TYPE: PSYCHIC, POWER: 60 },
    "Figy Berry": { TYPE: BUG, POWER: 60 },
    "Wiki Berry": { TYPE: ROCK, POWER: 60 },
    "Mago Berry": { TYPE: GHOST, POWER: 60 },
    "Aguav Berry": { TYPE: DRAGON, POWER: 60 },
    "Iapapa Berry": { TYPE: DARK, POWER: 60 },
    "Razz Berry": { TYPE: STEEL, POWER: 60 },
    "Bluk Berry": { TYPE: FIRE, POWER: 70 },
    "Nanab Berry": { TYPE: WATER, POWER: 70 },
    "Wepear Berry": { TYPE: ELECTRIC, POWER: 70 },
    "Pinap Berry": { TYPE: GRASS, POWER: 70 },
    "Pomeg Berry": { TYPE: ICE, POWER: 70 },
    "Kelpsy Berry": { TYPE: FIGHTING, POWER: 70 },
    "Qualot Berry": { TYPE: POISON, POWER: 70 },
    "Hondew Berry": { TYPE: GROUND, POWER: 70 },
    "Grepa Berry": { TYPE: FLYING, POWER: 70 },
    "Tamato Berry": { TYPE: PSYCHIC, POWER: 70 },
    "Cornn Berry": { TYPE: BUG, POWER: 70 },
    "Magost Berry": { TYPE: ROCK, POWER: 70 },
    "Rabuta Berry": { TYPE: GHOST, POWER: 70 },
    "Nomel Berry": { TYPE: DRAGON, POWER: 70 },
    "Spelon Berry": { TYPE: DARK, POWER: 70 },
    "Pamtre Berry": { TYPE: STEEL, POWER: 70 },
    "Watmel Berry": { TYPE: FIRE, POWER: 80 },
    "Durin Berry": { TYPE: WATER, POWER: 80 },
    "Belue Berry": { TYPE: ELECTRIC, POWER: 80 },
    "Occa Berry": { TYPE: FIRE, POWER: 60 },
    "Passho Berry": { TYPE: WATER, POWER: 60 },
    "Wacan Berry": { TYPE: ELECTRIC, POWER: 60 },
    "Rindo Berry": { TYPE: GRASS, POWER: 60 },
    "Yache Berry": { TYPE: ICE, POWER: 60 },
    "Chople Berry": { TYPE: FIGHTING, POWER: 60 },
    "Kebia Berry": { TYPE: POISON, POWER: 60 },
    "Shuca Berry": { TYPE: GROUND, POWER: 60 },
    "Coba Berry": { TYPE: FLYING, POWER: 60 },
    "Payapa Berry": { TYPE: PSYCHIC, POWER: 60 },
    "Tanga Berry": { TYPE: BUG, POWER: 60 },
    "Charti Berry": { TYPE: ROCK, POWER: 60 },
    "Kasib Berry": { TYPE: GHOST, POWER: 60 },
    "Haban Berry": { TYPE: DRAGON, POWER: 60 },
    "Colbur Berry": { TYPE: DARK, POWER: 60 },
    "Babiri Berry": { TYPE: STEEL, POWER: 60 },
    "Chilan Berry": { TYPE: NORMAL, POWER: 60 },
    "Liechi Berry": { TYPE: GRASS, POWER: 80 },
    "Ganlon Berry": { TYPE: ICE, POWER: 80 },
    "Salac Berry": { TYPE: FIGHTING, POWER:80 },
    "Petaya Berry": { TYPE: POISON, POWER:80 },
    "Apicot Berry": { TYPE: GROUND, POWER:80 },
    "Lansat Berry": { TYPE: FLYING, POWER:80 },
    "Starf Berry": { TYPE: PSYCHIC, POWER:80 },
    "Enigma Berry": { TYPE: BUG, POWER:80 },
    "Micle Berry": { TYPE: ROCK, POWER:80 },
    "Custap Berry": { TYPE: GHOST, POWER:80 },
    "Jaboca Berry": { TYPE: DRAGON, POWER:80 },
    "Rowap Berry": { TYPE: DARK, POWER:80 }
}

# Flavor Table
# Values
NP = 'NO_PREFERENCE'
LF = 'LIKE_FLAVOR'
DF = 'DISLIKE_FLAVOR'

# Flavors
SPICY = 'SPICY'
DRY = 'DRY'
SWEET = 'SWEET'
BITTER = 'BITTER'
SOUR = 'SOUR'

FLAVOR_LIKE = {
    SPICY: { BASHFUL: NP, ADAMANT: LF, BRAVE: LF, NAUGHTY: LF, LONELY: LF },
    DRY: { MODEST: LF, DOCILE: NP, QUIET: LF, RASH: LF, MILD: LF },
    SWEET: { TIMID: LF, JOLLY: LF, HARDY: NP, NAIVE: LF, HASTY: LF },
    BITTER: { CALM: LF, CAREFUL: LF, SASSY: LF, QUIRKY: NP, GENTLE: LF },
    SOUR: { BOLD: LF, IMPISH: LF, RELAXED: LF, LAX: LF, SERIOUS: NP }   
}

FLAVOR_DISLIKE = {
    SPICY: { BASHFUL: NP, MODEST: DF, TIMID: DF, CALM: DF, BOLD: DF },
    DRY: { ADAMANT: DF, DOCILE: NP, JOLLY: DF, CAREFUL: DF, IMPISH: DF },
    SWEET: { BRAVE: DF, QUIET: DF, HARDY: NP, SASSY: DF, RELAXED: DF },
    BITTER: { NAUGHTY: DF, RASH: DF, NAIVE: DF, QUIRKY: NP, LAX: DF },
    SOUR: { LONELY: DF, MILD: DF, HASTY: DF, GENTLE: DF, SERIOUS: NP }   
}

BERRY_CONDITIONS ={
    'Occa Berry': FIRE,
    'Passho Berry': WATER,
    'Wacan Berry': ELECTRIC,
    'Rindo Berry': GRASS,
    'Yache Berry': ICE,
    'Chople Berry': FIGHTING,
    'Kebia Berry': POISON,
    'Shuca Berry': GROUND,
    'Coba Berry': FLYING,
    'Payapa Berry': PSYCHIC,
    'Tanga Berry': BUG,
    'Charti Berry': ROCK,
    'Kasib Berry': GHOST,
    'Haban Berry': DRAGON,
    'Colbur Berry': DARK,
    'Babiri Berry': STEEL,
    'Chilan Berry': NORMAL
}

# MOVES WITH ADICIONAL EFFECTS
MOVES_CAN_CONFUSE = (
    'CHATTER'
)