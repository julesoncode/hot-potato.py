import curses 
import time
import random
from curses import textpad 


""" PAPA CALIENTE GAME WITH CURSES LIBRARY """

def get_potato_holder_index(game_player_list):
    for player in game_player_list:
        if player["has_potato"]: 
            return game_player_list.index(player)

def get_next_potato_holder_index(game_player_list):
    potato_holder_idx = get_potato_holder_index(game_player_list)
    if potato_holder_idx == len(game_player_list) - 1:  
        new_potato_holder_idx = 0 
    else:
        new_potato_holder_idx = potato_holder_idx + 1
    return(new_potato_holder_idx) 

def pass_potato(game_player_list):

    potato_holder = get_potato_holder_index(game_player_list)
    next_potato_holder = get_next_potato_holder_index(game_player_list)

    game_player_list[potato_holder]["has_potato"] = False #no longer holds the potato
    game_player_list[next_potato_holder]["has_potato"] = True 

def get_player_potato_coor(game_player_list):
    for player in game_player_list:
        if player["has_potato"]: 
            potato_coordinates = player["potato_coordinates"]
            return potato_coordinates 

def draw_game(stdscr, game_player_list, potato_color):    
    for player in game_player_list:
        plr_scr_coor = player["coordinates"] 
        plr_scr_y = plr_scr_coor[0]
        plr_scr_x = plr_scr_coor[1]
                
        stdscr.addch(plr_scr_y, plr_scr_x, curses.ACS_BLOCK, curses.color_pair(4))
        stdscr.addch(plr_scr_y, plr_scr_x + 1, curses.ACS_BLOCK, curses.color_pair(4))

        plr_str_y = plr_scr_y - 2
        plr_str_x = plr_scr_x - 3
        plr_tag = player["name"]

        stdscr.addstr(plr_str_y, plr_str_x, plr_tag, curses.color_pair(5))

        if player["has_potato"]:
            potato_scr_coor = player["potato_coordinates"]
            potato_scr_y = potato_scr_coor[0]
            potato_scr_x = potato_scr_coor[1]

            stdscr.addch(potato_scr_y, potato_scr_x, curses.ACS_DIAMOND, curses.color_pair(potato_color))

def hot_potato(stdscr, game_player_list):

    curses.curs_set(0) # Makes curser invisible

    # Initializes color pairs for player icons and potato color 
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_CYAN, -1)
    
    random.choice(game_player_list)["has_potato"] = True # Starting player 

    key = -1

    stdscr.timeout(1000//30)
        
    t = int(time.time())
    start_time = t
    p_end_time = start_time + 5 # Potato time
    g_end_time = start_time + 15 # Game time
    potato_color = 0

    while True:

        current_time = int(time.time()) 

        current_duration = current_time - start_time

        if current_duration < 5:
            potato_color = 1
        elif current_duration < 10:
            potato_color = 2
        else:
            potato_color = 3 

        if key != -1:
            pass_potato(game_player_list)
            p_end_time = current_time + 5
            
             
        # Draws player icons and potato 
        draw_game(stdscr, game_player_list, potato_color)

        if current_time >= p_end_time:
            loser_index = get_potato_holder_index(game_player_list)
            losing_player = game_player_list.pop(loser_index)
            return losing_player["name"]

        elif current_time >= g_end_time:
            loser_index = get_potato_holder_index(game_player_list)
            losing_player = game_player_list.pop(loser_index)
            return losing_player["name"]

        key = stdscr.getch()
        stdscr.clear() 


def display_menu():
        
    game_rules = """ 
###############################
#                             #
#       GAME CONTROLS         #
#                             #
###############################

You can: pass / keep / continue
--------------------------------

1.To PASS the potato press the 'SPACE' key
2.To KEEP the potato don't press anything!
3.To CONTINUE the round press the 'ENTER' Key 


###############################
#                             #
#      GAME INSTRUCTIONS      #
#                             #
###############################

Hot potato is a game that involves 
players gathering in a circle and 
tossing a small object such as a 
beanbag or even a real potato to 
each other while a 30 second timer 
goes off. The player who is holding 
the object when the timer stops is 
eliminated. The last player to remain 
in the game wins!

-----------------------------------
WATCH OUT FOR.... 

If you hold the potato for too long
your hands will melt (remember: it's
hot!). You have 5 seconds, before your
hands melt :-O

-----------------------------------
WIN THE GAME IF...

You have un-melted hands and you're
the last women standing!
"""

    menu_screen = """
    
###############################
#                             #
#       PAPA CALIENTE         #
#                             #
###############################

You can: view / start / quit  
----------------------------
[V]iew game controls and instructions 
[S]tart game
[Q]uit game

###############################
#                             #
#                             #
#                             #
###############################

        """
    while True:
        print(menu_screen)
        command = input("ACTION > ")
        command = command.upper()

        if command == "V":
            print(game_rules)
            print()
            other_command = input("Press the 'ENTER' key to go back: >")
        elif command == "S": 
            return "start"
        elif command == "Q":
            return "quit"

def play_game():

    while True:   

        action = display_menu()

        if action == "start":

            player_1 = {"coordinates": (3, 30),
                        "has_potato": False, 
                        "name": "Player 1", 
                        "potato_coordinates": (5,30)}  

            player_2 = {"coordinates": (10, 50),
                        "has_potato": False, 
                        "name": "Player 2", 
                        "potato_coordinates": (12, 50)}

            player_3 = {"coordinates": (18, 30),
                        "has_potato": False, 
                        "name": "Player 3", 
                        "potato_coordinates": (20,30)}

            player_4 = {"coordinates":(10, 12),
                        "has_potato": False, 
                        "name": "Player 4", 
                        "potato_coordinates":(12, 12)}

            game_player_list = [player_1, player_2, player_3, player_4]  
            
            while True:
                game_win_lose = curses.wrapper(hot_potato, game_player_list) # Starts game

                if len(game_player_list) == 1:
                    print("""

###############################
#                             #
#         WINNER!             #
#                             #
###############################
                         
    {} has WON the game!   
                            
###############################
#                             #
#         WINNER!             #
#                             #
###############################

                    """.format(game_win_lose))
                    break
                elif len(game_player_list) > 1:
                    print("""

###############################
#                             #
#         TIMES UP!           #
#                             #
###############################
              
    {} is OUT the game! 
                            
###############################
#                             #
#         TIMES UP!           #
#                             #
###############################

                    """.format(game_win_lose))
                    input("""
                    
                    Press 'ENTER' key to continue: >""").upper()
        elif action == "quit":
            print("Quit game")
            break
play_game()
