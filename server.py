import socket
import threading
import time
import itertools
import random
import json
from typing import List
from typing import Optional
import utils
import os
import const as CONST

class Game:
    def __init__(self, total_users: int):
        self.total_users = total_users
        self.curr_users = 0
        self.uuid = 0
        self.turns = itertools.cycle([i for i in range(1, total_users+1)])
        self.turn = next(self.turns)
        self.connections = set()
        self.scoreboard = [[0]*12 for _ in range(total_users+1)]
        self.status = None
        self.curr_data = None

    def roll(self, dices: list[int], fixed_index=list[bool]):
        for i in range(len(fixed_index)):
            if not fixed_index[i]:
                dices[i] = random.randint(1, 6)
        return dices
    
    def end_turn(self):
        self.turn = next(self.turns)
    
def handle_client(client_socket, client_address, uuid):
    try:
        recv_data = client_socket.recv(1024)
        # game.connections.add((uuid, client_socket, client_address))
        # print(uuid, client_socket, client_address)
        # print(recv_data.decode())
        while True:
            if game.curr_users < game.total_users:
                client_socket.sendall(utils.encode_server_data("PREGAME"))
            else:
                if game.turn == uuid:
                    client_socket.sendall(utils.encode_server_data("TURN", 3, [0]*5, [False]*5))
                else:
                    client_socket.sendall(utils.encode_server_data("WAIT", 3, [0]*5, [False]*5))
                    game.status = 'WAIT'
                is_turn = True
                while is_turn:
                    if game.turn == uuid:
                        data = client_socket.recv(1024)
                        recv_data = utils.decode_client_data(data)
                        game.curr_data = recv_data
                        match recv_data["status"]:
                            case "ROLL":
                                print(recv_data)
                                dices = game.roll(recv_data['data']['dice'], recv_data['data']['fixed_index'])
                                client_socket.sendall(utils.encode_server_data("TURN", 2, dices, recv_data['data']['fixed_index']))
                                
                            case "END_TURN":
                                print(f'{uuid}\n{recv_data}\n{game.scoreboard}')
                                game.scoreboard[uuid][recv_data['data']['score_index']] = recv_data['data']['score']
                                print(game.scoreboard)
                                game.end_turn()
                                is_turn = False
                    else:
                        curr_player_data = game.curr_data
                        if curr_player_data:
                            match recv_data["status"]:
                                case "ROLL":
                                    client_socket.sendall(utils.encode_server_data("WAIT", recv_data['data']['remaining_roll']-1, curr_player_data['data']['dice']))
                                    
                                case "END_TURN":
                                    client_socket.sendall(utils.encode_server_data("WAIT", 0, curr_player_data['data']['dice']))
                                    is_turn = False
                             
                    time.sleep(1)
                
            time.sleep(1)
            

    finally:
        print(f"Closing connection with user {uuid} on {client_address}.")
        client_socket.close()

def run_server():
    IP, PORT = '127.0.0.1', CONST.PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)

    print(f"Server Initialized on {PORT}")

    try:
        while game.uuid < game.total_users:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            game.uuid += 1
            game.curr_users += 1

            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, game.uuid))
            client_handler.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == '__main__':
    global game
    game = Game(1)
    run_server()