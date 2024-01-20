import socket
import threading
import time
import itertools
import random
import json
from typing import List
from typing import Optional
import utils

class Game:
    def __init__(self, total_users: int):
        self.total_users = total_users
        self.curr_users = 0
        self.uuid = 0
        self.turns = itertools.cycle([i for i in range(1, total_users+1)])
        self.turn = next(self.turns)
        self.connections = {}
        self.scoreboard = [[0]*12 for _ in range(total_users)]

    def roll(self, dices: List[int], indices: List[int]):
        for i in indices:
            dices[i] = random.randint(1, 6)
        return dices
    
    def end_turn(self):
        self.turn = next(self.turns)
    
def handle_client(client_socket, client_address, uuid):
    try:
        recv_data = client_socket.recv(1024)
        print(recv_data.decode())
        while True:
            if game.curr_users < game.total_users:
                client_socket.sendall(utils.encode_server_data("PREGAME"))
            else:
                if game.turn == uuid:
                    client_socket.sendall(utils.encode_server_data("TURN", 3, [1,2,3,4,5]))
                else:
                    client_socket.sendall(utils.encode_server_data("WAIT", 3, [1,2,3,4,5]))
                
                data = client_socket.recv(1024)
                recv_data = utils.decode_client_data(data)
                
                match recv_data["status"]:
                    case "ROLL":
                        dices = game.roll(recv_data['data']['dice'], recv_data['data']['index'])
                        client_socket.sendall(utils.encode_server_data("TURN", 2, dices))
                    case "END_TURN":
                        game.scoreboard[recv_data['data']['index']] = recv_data['data']['score']
                        game.end_turn()
            time.sleep(1)
            

    finally:
        print(f"Closing connection with user{uuid} on {client_address}.")
        client_socket.close()

def run_server():
    IP, PORT = '127.0.0.1', 3000
    
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
    game = Game(2)
    run_server()