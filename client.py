import socket
import json
from collections import Counter

class player:
    def __init__(self, server):
        self.score: int = 0
        self.opponent_score: int = 0
        self.used_board_index = set()
        self.scoreboard: list[int] = []
        self.server = server
        self.turn = False
        self.dict_scoreboard = {0: "0. Ones:",
                                1: "1. Twos:",
                                2: "2. Threes:",
                                3: "3. Fours:",
                                4: "4. Fives:",
                                5: "5. Sixs:",
                                6: "6. Full House:",
                                7: "7. Four-Of-A-Kind:",
                                8: "8. Little Straight:",
                                9: "9. Big Straigt:", 
                                10: "10. Choice:",
                                11: "11. Yacht:"}
        

    """ TODO: player will make a move. First decide wheather to end_my_turn/
    if no reroll_remaining, end_my_turn and send score to the server.
    Otherwise, We can assume player want to reroll at least some of dice."""
    def make_move(self, end_my_turn: bool, reroll_remaining: int, dice: list[int], reroll_dice: list[bool]):
        if reroll_remaining == 3:
            data = {
                "STATUS": "ROLL",
                "DATA": {
                    "dice": [0,0,0,0,0],
                    "index": [True, True, True, True, True],
                },
                "MSG": "",
            }
        
        elif end_my_turn or not reroll_remaining:
            # have to make player choose score from possible_scores
            possible_scores = self.select_score(dice)
            print(possible_scores)
            index = [i for i in range(12)]
            possible_out = []
            for i, score in zip(index, possible_scores):
                if score != -1:
                    possible_out.append([self.dict_scoreboard[i], score])
            print(possible_out)
            selected_score_index = int(input("Select Index: "))
            selected_score = possible_scores[selected_score_index]
            while selected_score_index < 0 or selected_score_index > 11 or selected_score_index in self.used_board_index:
                print("Possible Index are:", [i for [i,k] in possible_out]) 
                selected_score_index = input("Select different Index: ")
                selected_score = possible_scores[selected_score_index]
            data = {
                "STATUS": "END TURN",
                "DATA": {
                    "index": selected_score_index,
                    "score": selected_score,
                },
                "MSG": "",
            }
            
        else:
            # make user to chose which index they want to reroll
            data = {
                "STATUS": "ROLL",
                "DATA": {
                    "dice": dice,
                    "index": reroll_dice,
                },
                "MSG": "",
            }
        json_data = json.dumps(data, indent = 4)
        self.server.sendall(json_data.encode())
        return None

    
    """ TODO: Player will be shown the possible score board to choose from.
    input: current state of dice
    output: 12 possible combination of score"""
    def select_score(self, dice: list[int]) -> list[int]:
        yacht_scoreboard = [0 for i in range(12)]
        print(dice)
        for i in range(12):
            # selected score can not be chosen again.
            if i in self.used_board_index:
                yacht_scoreboard[i] = -1
            else:
                if i == 0:
                    yacht_scoreboard[i] = sum([1 for die in dice if die == 1])
                elif i == 1:
                    yacht_scoreboard[i] = sum([2 for die in dice if die == 2])
                elif i == 2:
                    yacht_scoreboard[i] = sum([3 for die in dice if die == 3])
                elif i == 3:
                    yacht_scoreboard[i] = sum([4 for die in dice if die == 4])
                elif i == 4:
                    yacht_scoreboard[i] = sum([5 for die in dice if die == 5])
                elif i == 5:
                    yacht_scoreboard[i] = sum([6 for die in dice if die == 6])
                # full-house
                elif i == 6:
                    full_house = True if len(Counter(dice)) == 2 else False
                    yacht_scoreboard[i] = sum(dice) if full_house else 0
                # Four-of-a-Kind
                elif i == 7:
                    result = [num for num, count in Counter(dice).items() if count == 4]
                    yacht_scoreboard[i] = result[0] * 4 if len(result) == 1 else 0
                # Little Straight
                elif i == 8:
                    dice.sort()
                    found_litte_straight = True
                    for j in range(len(dice)):
                        if j != dice[j]:
                            found_litte_straight = False
                            break
                    yacht_scoreboard[i] = 30 if found_litte_straight else 0
                # Big Straight
                elif i == 9:
                    dice.sort()
                    found_big_straight = True
                    for j in range(len(dice)):
                        if j + 1 != dice[j]:
                            found_big_straight = False
                            break
                    yacht_scoreboard[i] = 30 if found_big_straight else 0

                #Choice: Sum of all dice
                elif i == 10:
                    yacht_scoreboard[i] = sum(dice)
                #Yacht: all five dice showing the same face
                else:
                    yacht_scoreboard[i] = 50 if len(Counter(dice)) == 1 else 0

        return yacht_scoreboard
        

if __name__ == '__main__':
    # Player setup
    SERVER_IP = "135.180.100.66"
    PORT = 3000

    # test = player("server")
    # print(test.make_move(False, 1, [1,1,2,3,6], [False,False,False,False,False]))

    # data = {
    #             "STATUS": "ROLL",
    #             "DATA": {
    #                 "dice": [0,0,0,0,0],
    #                 "index": [True, True, True, True, True],
    #             },
    #             "MSG": "",
    #         }

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((SERVER_IP, PORT))
        print("You Have Successfully Connected to the Server")

        # json_data = json.dumps(data, indent = 4)
        # server.sendall(json_data.encode())
        p = player(server)

        while True:
            try:
                data = server.recv(4096).decode()
                prev_data = None  
                if prev_data != data:
                    json_data = json.loads(data)

                    if json_data["STATUS"] == "PREGAME":
                        print("WAITING FOR THE OPPONENT.")
                    
                    elif json_data["STATUS"] == "TURN":
                        p.turn = True
                        
                        # make_move(self, end_my_turn: bool, reroll_remaining: int, dice: list[int], reroll_dice: list[bool])
                        dice = json_data["DATA"]["dice"]
                        remain = json_data["DATA"]["remaining_roll"]

                        if remain == 3:
                            move = input("CHOOSE YOUR MOVE: POSSIBLE MOVE: (0. ROLL): ")
                            p.make_move(False, 3, dice, [True for i in range(5)])

                        elif remain == 1 or remain == 2:
                            print("CHOOSE YOUR MOVE:\n")
                            move = input("POSSIBLE MOVE: \n(0. REROLL) \n(1, STOP & SELECT SCORE) ")
                            move = 0 if move == 0 or move == "REROLL" or move == "Reroll" or move == "reroll" else 1
                            if move == 0:
                                while True:
                                    print("Current Dice: ", dice)
                                    print("WHICH INDEX WOULD YOU LIKE TO REROLL:\n")
                                    move = input("PLEASE INPUT EACH INDEX SEPEARTED WITH SPACE: ")
                                    print("IS THIS CORRECT:\n")
                                    br = input(move.split(" "), "Y/N")
                                    if br == "Y" or br == "y" or br == "Yes" or br == "yes":
                                        break
                                
                                chosen_index = [int(i) for i in move.split(" ")]
                                p.make_move(False, remain, dice, [True for i in range(5) if i in chosen_index])
                            else:
                                p.make_move(True, remain, dice, [False, False, False, False, False])
                        else:
                            p.make_move(False, remain, dice, [False, False, False, False, False])
                            # p.make_move()
                    elif json_data["STATUS"] == "WAIT":
                        print("WAIT FOR THE OPPONENT TO END HIS/HER TURN")

                        """TODO: Need to work on updating and displaying Opponents' progress"""

                    elif json_data["STATUS"]  == "END":
                        print(json_data["MSG"])
                        break
                    prev_data = data
                

            except json.JSONDecodeError:
                print("Received Data is not in JSON format.")
                break
    except:
        print("You Have Failed to Connect")