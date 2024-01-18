# import socket
# import time

# def run_client():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('127.0.0.1', 3000))

#     try:
#         while True:
#             client_socket.sendall("hi from Berkeley".encode())
#             # Get player's move (rock, paper, scissors, or exit) from user input
#             # move = input(f"{player_name}, enter your move (rock, paper, scissors, or exit to leave): ")

#             # Send the move to the server
#             # client_socket.sendall(move.encode())
#             # print(f"Sent to server: {move}")

#             # Receive and print the server's response
#             response = client_socket.recv(1024).decode()
#             print(f"Received from server: {response}")

#             # if move.lower() == "exit":
#                 # break  # If the player exits, end the game for that player

#             # Simulate a delay (1 second) before the next move
            

#     finally:
#         print(f"Closing connection with the server.")
#         client_socket.close()

# if __name__ == '__main__':
#     run_client()
    
import socket
import json
from player import Player
from collections import Counter


if __name__ == '__main__':
    # Player setup
    SERVER_IP = "127.0.0.1"
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
        p = Player(server)
        ip = socket.gethostbyname(socket.gethostname())
        server.sendall(f"Connected ACK from {ip}".encode())

        while True:
            try:
                data = server.recv(4096).decode()
                prev_data = None  
                print("not here?")
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