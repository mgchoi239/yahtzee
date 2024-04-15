import socket
import json
from player import Player
from collections import Counter
import utils
import art
import os
import dice as diceroll
import const as CONST

def valid_input(msg, valid_set, ipt_type):
    ipt = ipt_type(input(msg).lower())
    while ipt not in valid_set:
        print(f"\n>> NOT A VALID INPUT << ({valid_set})")
        ipt = input(msg)
    return ipt

if __name__ == '__main__':
    # Player setup
    SERVER_IP = "127.0.0.1"
    PORT = CONST.PORT


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
        os.system('clear')
        print(art.LOGO)
        
        while True:
            try:
                data = server.recv(4096)
                recv_data = utils.decode_client_data(data)
                prev_data = None  
                if prev_data != recv_data:
                    # print(recv_data)
                    # print(recv_data["msg"])
                    match recv_data["status"]:
                        case "PREGAME":
                            print("WAITING FOR OTHER PLAYERS...")
                        case "TURN":
                            p.turn = True
                            # make_move(self, end_my_turn: bool, reroll_remaining: int, dice: list[int], reroll_dice: list[bool])
                            dice = recv_data["data"]["dice"]
                            remain = recv_data["data"]["remaining_roll"]
                            fixed_index = recv_data["data"]["fixed_index"]

                            diceroll.show_dice(dice)

                            match remain:
                                case 3:
                                    move = valid_input("ENTER YOUR MOVE:\n(0: ROLL):\n",{'0', 'roll'},str)
                                    # move = input("ENTER YOUR MOVE:\n(0: ROLL):\n")
                                    p.make_move(False, 3, dice, fixed_index)
                                case 2 | 1:
                                    print("CHOOSE YOUR MOVE:\n")
                                    move = valid_input("POSSIBLE MOVES: \n(0: REROLL) \n(1: STOP & SELECT SCORE)\n", {'0','1'}, str)
                                
                                    # move = 0 if move == 0 or move == "REROLL" or move == "Reroll" or move == "reroll" else 1
                                    if move == '0':
                                        print("Current Dice: ", dice)
                                        print("WHICH INDEX WOULD YOU LIKE TO FIX:\n")
                                        move = input("PLEASE INPUT EACH INDEX SEPEARTED WITH SPACE: ")
                                        confirm = valid_input("IS {} CORRECT:\n".format(move), {'y', 'n'}, str)

                                        if confirm == 'y':
                                            print(f'initial: {fixed_index}')
                                            for str_i in move.split(" "):
                                                fixed_index[int(str_i)] = True
                                            print(f'final: {fixed_index}')
                                            p.make_move(False, remain, dice, fixed_index)
                                    else:
                                        p.make_move(True, remain, dice, [True]*5)
                                case 0:
                                    """
                                    TODO:
                                    remain == 1 will be the last time the user will be able to make any moves.
                                    remain == 0 is an announcement by the server; no user action required besides printing information
                                    """
                                    print("Move finished. Current Scores are: ")
                                    # p.make_move(False, remain, dice, [False, False, False, False, False])
                                    # p.make_move()
                        case "WAIT":
                            """
                            TODO: Need to work on updating and displaying Opponents' progress
                            """
                            data = server.recv(4096)
                            recv_data = utils.decode_client_data(data)
                            if recv_data:
                                p.turn = False
                                dice = recv_data["data"]["dice"]
                                remain = recv_data["data"]["remaining_roll"]
                                print(f'Other player just rolled. They have {remain} rolls remaining and received the following dices')
                                diceroll.show_dice(dice)

                        case "END":
                            break
                                    
                    prev_data = recv_data

            except json.JSONDecodeError:
                print("Received Data is not in JSON format.")
                break
    except:
        print("You Have Failed to Connect")