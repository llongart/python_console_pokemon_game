from functions import get_database, initialize_game, startbattle, savegame

# Start battle
get_database()
battle = initialize_game()    
startbattle(battle)
savegame(battle.player1, battle.player2)