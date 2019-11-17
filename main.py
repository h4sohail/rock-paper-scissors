from modules.game import Game # /modules/game.py
from modules.actors import Player, AiPlayer # /modules/actors.py
from modules.draw import DrawData # /modules/draw.py



# main function
def main():
    game = Game()  # initialize the Game object
    human = Player()  # initialize the Player object
    ai = AiPlayer()  # initialize the AiPlayer object
    
    (player_data, ai_data, game_data, loaded) = game.load_game() # ask to load the previous game (load_game() returns a tuple of 4 elements)
    
    if loaded == True: # only load data if game.load_game() ran succesfully
        human.name = player_data['name'] # get the human name from the player data dict
        human.wins = player_data['wins'] # get the human wins from the player data dict
        human.win_rate = player_data['win_rate'] # get the win rate from the player data dict
        ai.name = ai_data['name'] # get the ai name from the ai data dict
        ai.wins = ai_data['wins'] # get the ai wins from the ai data dict
        ai.win_rate = ai_data['win_rate'] # get the ai win rate from the ai data dict
        game.sessions = game_data['sessions'] # get the game sessions data from game data dict
        print('Loaded succesfully')

    while (game.get_state() == True):  # keep looping if the game state is True
        
        human.set_choice()  # set human choice

        if human.choice not in game.options:  # check the input and break the loop if the input is not what we want
            print('Error 1: Incorrect input')
            continue

        human.history.append(human.choice) # add player choices to a list

        if human.choice == 'exit':
            game.close()
            continue
        
        game.sessions += 1  # track game sessions
        def matrixFreq():
            rFreq = [[0,0,0],[0,0,0],[0,0,0]]
            pFreq = [[0,0,0],[0,0,0],[0,0,0]]
            sFreq = [[0,0,0],[0,0,0],[0,0,0]]

            def convertToIndex(move):
                for i in range(len(move)):
                    if move[i] == "rock":
                        move[i] = 0
                    elif move[i] == "paper":
                        move[i] = 1
                    else:
                        move[i] = 2
                return move
            last2Move = [ai.get_second_last_choice(), human.get_second_last_choice()]
            # print(ai.get_last_choice(),human.get_last_choice())
            last2Move = convertToIndex(last2Move)

            if human.get_last_choice() == "rock":
                #ai is row, human is col
                # print(last2Move)
                rFreq[last2Move[0]][last2Move[1]] += 1
            if human.get_last_choice() == "paper":
                pFreq[last2Move[0]][last2Move[1]] += 1

            if human.get_last_choice() == "scissors":
                sFreq[last2Move[0]][last2Move[1]] += 1

            #compare freq
            predict = [ai.get_last_choice(),human.get_last_choice()]
            predict = convertToIndex(predict)

            large = [rFreq[predict[0]][predict[1]], pFreq[predict[0]][predict[1]],sFreq[predict[0]][predict[1]]]

            if max(large) == 0:
                ai.set_choice() #random move if no pattern
            else:
                prefer_next_move = large.index(max(large))
                if prefer_next_move == 0: 
                    ai.choice = "paper" #play counter
                elif prefer_next_move == 1:
                    ai.choice = "scissors"
                else:
                    ai.choice = "rock"

        def win_stay_lose_shift():
            if len(game.wins) > 0:
                if game.wins[-1] == "human": #play counter of previous human winning move
                    print(human.get_last_choice(),"%")
                    if human.get_last_choice == "paper":
                        ai.choice = "scissors"
                    elif human.get_last_choice == "scissors":
                        ai.choice = "rock"
                    else:
                        ai.choice = "paper"
                else: #human loses, change. Play counter of the other possible hands
                    moves = ["rock","paper","scissors"]
                    moves.remove(human.get_last_choice())
                    possible_next_move = moves[random.randint(0,1)] #random 
                    if possible_next_move == "rock":
                        ai.choice = "paper"
                    elif possible_next_move == "paper":
                        ai.choice = "scissors"
                    else:
                        ai.choice = "rock"
            else:
                ai.set_choice()
        

        if game.sessions == 1: # if it's the first round
            ai.set_choice()  # set the ai choice (randomly)
        
        print('------------------------')

        print(f'{human.name} selected: {human.choice}') # display the player choice
        print(f'{ai.name} selected: {ai.choice}') # display the ai choice

        # compare the choices and display the winner
        if ai.choice == human.choice:
            print('[Draw]')

        elif ai.choice == 'rock' and human.choice == 'scissors':
            print(f'[{ai.name} won]')
            ai.wins += 1 # increment ai win by 1

        elif ai.choice == 'paper' and human.choice == 'rock':
            print(f'[{ai.name} won]')
            ai.wins += 1 # increment ai win by 1

        elif ai.choice == 'scissors' and human.choice == 'paper':
            print(f'[{ai.name} won]')
            ai.wins += 1 # increment ai win by 1

        else:
            print(f'[{human.name} won]')
            human.wins += 1 # increment player win by 1

        print('------------------------')

        ai.win_rate.append(ai.wins / game.sessions) # track the ai win rate
        human.win_rate.append(human.wins / game.sessions) # track the player win rate

    # player, ai and game data is saved in dictionaries for the purpose of saving
    player_data = {"name": human.name, "wins": human.wins, "win_rate": human.win_rate}
    ai_data = {"name": ai.name, "wins": ai.wins, "win_rate": ai.win_rate}
    game_data = {"sessions": game.sessions}
    
    print(f'SCORES ---- Humans: {human.wins} AI: {ai.wins}') # display the individual wins
    print(f'AI Win Rate: {ai.get_win_rate()}%') # display the ai win rate 
    print(f'HUMAN Win Rate: {human.get_win_rate()}%') # display the player win rate

    save_status = game.save_game(player_data, ai_data, game_data) # asks to save the game
    if save_status == True: # print a message if saved succesfully
        print('Saved game succesfully')


# entry point
if __name__ == '__main__':
    main()
