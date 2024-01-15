import socket
import json
from collections import Counter

class player:

    def __init__(self, player_turn):
        self.score: int = 0
        self.opponent_score: int = 0
        self.used_board_index = set()
        self.scoreboard: list[int] = []
        self.player_turn: bool = player_turn

    """ TODO: player will make a move. First decide wheather to end_my_turn/
    if no reroll_remaining, end_my_turn and send score to the server.
    Otherwise, We can assume player want to reroll at least some of dice."""
    def make_move(self, end_my_turn: bool, reroll_remaining: int, dice: list[int], reroll_dice: list[bool]):
        if end_my_turn or not reroll_remaining:
            # have to make player choose score from possible_scores
            possible_scores = self.select_score(dice)
        else:
            return None

    
    """ TODO: Player will be shown the possible score board to choose from.
    input: current state of dice
    output: 12 possible combination of score"""
    def select_score(self, dice: list[int]) -> list[int]:
        yacht_scoreboard = [0 for i in range(12)]

        for i in range(12):
            # selected score can not be chosen again.
            if i in self.used_board_index:
                yacht_scoreboard[i] = -1
            else:
                if i == 0:
                    yacht_scoreboard[i] = sum([1 for i in dice if i == 1])
                elif i == 1:
                    yacht_scoreboard[i] = sum([2 for i in dice if i == 2])
                elif i == 2:
                    yacht_scoreboard[i] = sum([3 for i in dice if i == 3])
                elif i == 3:
                    yacht_scoreboard[i] = sum([4 for i in dice if i == 4])
                elif i == 4:
                    yacht_scoreboard[i] = sum([5 for i in dice if i == 5])
                elif i == 5:
                    yacht_scoreboard[i] = sum([6 for i in dice if i == 6])
                # full-house
                elif i == 6:
                    full_house = False if len(Counter(dice).keys) else True
                    yacht_scoreboard[i] = sum(dice) if full_house else 0
                # Four-of-a-Kind
                elif i == 7:
                    result = next((num for num, count in Counter(dice).items() if count == 4), None)
                    yacht_scoreboard[i] = result * 4
                # Little Straight
                elif i == 8:
                    dice.sort()
                    found_litte_straight = True
                    for i in range(len(dice)):
                        if i != dice[i]:
                            found_litte_straight = False
                            break
                    yacht_scoreboard[i] = 30 if found_litte_straight else 0
                # Big Straight
                elif i == 9:
                    dice.sort()
                    found_big_straight = True
                    for i in range(len(dice)):
                        if i + 1 != dice[i]:
                            found_big_straight = False
                            break
                    yacht_scoreboard[i] = 30 if found_big_straight else 0

                #Choice: Sum of all dice
                elif i == 10:
                    yacht_scoreboard[i] = sum(dice)
                #Yacht: all five dice showing the same face
                else:
                    yacht_scoreboard[i] = 50 if len(Counter(dice).keys) == 1 else 0

        return yacht_scoreboard
        

if __name__ == '__main__':
    # Player setup
    
    SERVER_IP = "135.180.100.66"
    PORT = 3001

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((SERVER_IP, PORT))
        print("You Have Successfully Connected to the Server")
        message = input("Enter Player Name: ")

        # print("Waiting for Opponet...")
        # find a way to hold at this point
        
        # when server finds oppoents set two player's attribue (myturn) to True/False
        my_turn = False # this need to be received by the server
        p = player(my_turn)
        winner = None

        while not winner:
            if my_turn:
                p.make_move()


    except:
        print("You Have Failed to Connect")


# import socket

# # Player 2 setup
# PLAYER1_IP = "135.180.100.66"
# PORT = 3001       # Choose a port number

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player2_socket:
#     player2_socket.connect((PLAYER1_IP, PORT))

#     while True:
#         message = input("Enter your move: ")
#         player2_socket.sendall(message.encode())

#         data = player2_socket.recv(1024).decode()
#         print(f"Player 2: Received - {data}")