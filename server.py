import socket
import json

class Game:
    def __init__(self, player):
        self.player_count: int = player
        self.ports: list = [p for p in range(3000, 3000+player)]

def handle_player(i):
    PORT = 3000+i
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player_socket:
        player_socket.bind(('0.0.0.0', PORT))
        player_socket.listen()

        print(f"Player {i} listening on port {PORT}")
        # Accept connection from Player X
        conn, addr = player_socket.accept()
        with conn:
            print(f"Player {i} connected by {addr} via {PORT}")

            info = {"STATUS": "PREGAME", "DATA":"", "MSG":"Waiting for other players..."}
            conn.sendall(json.loads(info).encode())

def start_server(game):
    for i in range(game.player_count):
        handle_player(i)  

if __name__ == '__main__':
    game = Game(2)
    start_server(game)