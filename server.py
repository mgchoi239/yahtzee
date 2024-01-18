import socket
import threading
import time
import itertools
import random
import json
from typing import List

class Game:
    def __init__(self, total_users: int):
        self.total_users = total_users
        self.uuid = 0
        self.turns = itertools.cycle([i for i in range(1, total_users+1)])
        self.turn = next(self.turns)
        self.connections = {}

    def roll(self, dices: List[int], indices: List[int]):
        for i in indices:
            dices[i] = random.randint(1, 6)
        return dices
    
    def end_turn(self):
        self.turn = next(self.turns)

class ServerData:
    def __init__(self, status: str, remaining_roll=None, dice=None):
        self.status = status
        self.data = {}
        self.msg = None
        match status:
            case "PREGAME":
                self.msg = "Waiting for other players..."
            case "TURN":
                self.data["remaining_roll"]=remaining_roll
                self.data["dice"]=dice
                self.msg = f"You have {remaining_roll} remaining"
            case "WAIT":
                self.remaining_roll = remaining_roll
                self.dice = dice
                self.msg = f"Currently other player's roll"
            case "END":
                self.msg = "You won!"
    
    def encode_server_data(self):
        data = {"STATUS":self.status, "DATA":self.data, "MSG":self.msg}
        json_data = json.dumps(data, indent = 4) 
        return json_data.encode()

def handle_client(client_socket, client_address, uuid):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode())
            if game.uuid < game.total_users:
                data = ServerData("PREGAME")
                client_socket.sendall(data.encode_server_data())
            else:
                if game.turn == uuid:
                    data = ServerData("TURN", 3, [1,2,3,4,5])
                    client_socket.sendall(data.encode_server_data())
                else:
                    data = ServerData("WAIT", 3, [1,2,3,4,5])
                    client_socket.sendall(data.encode_server_data())

            time.sleep(1)

    finally:
        print(f"Closing connection with user{uuid} on {client_address}.")
        client_socket.close()

def run_server():
    IP, PORT = '127.0.0.1', 3000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)

    print("Server Initialized on 3000")

    try:
        while game.uuid < game.total_users:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            game.uuid += 1

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