import socket
import json
from collections import Counter
import utils
import art
import dice as diceroll
# import client as client

def valid_input_int(msg, valid_set):
    # print(msg)
    # print(valid_set)
    # ipt = input()
    # while not ipt.isnumeric and int(ipt) not in valid_set:
    #     print(f"\n>> NOT A VALID INPUT << ({valid_set})")
    #     ipt = input()
    # return ipt

    ipt = input(msg).lower()
    print(ipt, type(ipt))
    while not ipt.isnumeric() or int(ipt) not in valid_set:
        print(f"\n>> NOT A VALID INPUT << ({valid_set})")
        ipt = input(msg)
    print('passed')
    return int(ipt)

class Player:
    def __init__(self, server):
        self.score: int = 0
        self.opponent_score: int = 0
        self.unused_board_index = set([i for i in range(12)])
        self.scoreboard: list[int] = [0]*12
        self.server = server
        self.turn = False
        self.dict_scoreboard = {0: "(0) Ones:",
                                1: "(1) Twos:",
                                2: "(2) Threes:",
                                3: "(3) Fours:",
                                4: "(4) Fives:",
                                5: "(5) Sixes:",
                                6: "(6) Full House:",
                                7: "(7) Four-Of-A-Kind:",
                                8: "(8) Little Straight:",
                                9: "(9) Big Straight:", 
                                10: "(10) Choice:",
                                11: "(11) Yacht:"}
        

    """ TODO: player will make a move. First decide wheather to end_my_turn/
    if no reroll_remaining, end_my_turn and send score to the server.
    Otherwise, We can assume player want to reroll at least some of dice."""
    def make_move(self, end_my_turn: bool, roll_remaining: int, dice: list[int], fixed_index: list[bool]):
        
        print(end_my_turn, roll_remaining, dice, fixed_index)
        if roll_remaining == 3:
            self.server.sendall(utils.encode_client_data(status="ROLL", remaining_roll=roll_remaining, dice=[0]*5, fixed_index=[False]*5))
            diceroll.roll_dice(dice, fixed_index)
            
        elif end_my_turn or not roll_remaining:
            # have to make player choose score from possible_scores
            possible_scores = self.select_score(dice)
            print(possible_scores)
            
            possible_out = [score if score != -1 else -1 for score in possible_scores]
            print(art.TABLE.format(*possible_out))
            
            selected_score_index = valid_input_int("Select Index:\n", self.unused_board_index) 
            selected_score = possible_scores[selected_score_index]
            self.unused_board_index.remove(selected_score_index)
            
            print(f'----\n{selected_score}\n{selected_score_index}\n{fixed_index}')
            
            self.server.sendall(utils.encode_client_data(status="END_TURN", remaining_roll=roll_remaining, score=selected_score, score_index=selected_score_index, fixed_index=fixed_index))
            
        else:
            # make user to chose which index they want to reroll
            print("loading reroll")
            print()
            self.server.sendall(utils.encode_client_data(status="ROLL", remaining_roll=roll_remaining, dice=dice, fixed_index=fixed_index))
            diceroll.roll_dice(dice, fixed_index)

    
    """ TODO: Player will be shown the possible score board to choose from.
    input: current state of dice
    output: 12 possible combination of score"""
    def select_score(self, dice: list[int]) -> list[int]:
        yacht_scoreboard = [0 for i in range(12)]
        print(dice)
        for i in range(12):
            # selected score can not be chosen again.
            if i not in self.unused_board_index:
                yacht_scoreboard[i] = -1
            match i:
                case 0:
                    yacht_scoreboard[i] = sum([1 for die in dice if die == 1])
                case 1:
                    yacht_scoreboard[i] = sum([2 for die in dice if die == 2])
                case 2:
                    yacht_scoreboard[i] = sum([3 for die in dice if die == 3])
                case 3:
                    yacht_scoreboard[i] = sum([4 for die in dice if die == 4])
                case 4:
                    yacht_scoreboard[i] = sum([5 for die in dice if die == 5])
                case 5:
                    yacht_scoreboard[i] = sum([6 for die in dice if die == 6])
                # full-house
                case 6:
                    full_house = True if len(Counter(dice)) == 2 and 0 not in dice else False
                    yacht_scoreboard[i] = sum(dice) if full_house else 0
                # Four-of-a-Kind
                case 7:
                    result = [num for num, count in Counter(dice).items() if count == 4]
                    yacht_scoreboard[i] = result[0] * 4 if len(result) == 1 else 0
                # Little Straight
                case 8:
                    dice.sort()
                    found_litte_straight = True
                    for j in range(len(dice)):
                        if j != dice[j]:
                            found_litte_straight = False
                            break
                    yacht_scoreboard[i] = 30 if found_litte_straight else 0
                # Big Straight
                case 9:
                    dice.sort()
                    found_big_straight = True
                    for j in range(len(dice)):
                        if j + 1 != dice[j]:
                            found_big_straight = False
                            break
                    yacht_scoreboard[i] = 30 if found_big_straight else 0

                #Choice: Sum of all dice
                case 10:
                    yacht_scoreboard[i] = sum(dice)
                #Yacht: all five dice showing the same face
                case 11:
                    yacht_scoreboard[i] = 50 if len(Counter(dice)) == 1 else 0

        return yacht_scoreboard