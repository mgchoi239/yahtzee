# import socket
# import json
# import asyncio

# class Game:
#     def __init__(self, player):
#         self.player_count: int = player

# def handle_player(connections, i):
#     PORT = 3000+i
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player_socket:
#         player_socket.bind(('0.0.0.0', PORT))
#         player_socket.listen()

#         print(f"Player {i} listening on port {PORT}")
#         # Accept connection from Player X
#         conn, addr = player_socket.accept()
#         with conn:
#             print(f"Player {i} connected by {addr} via {PORT}")

#             info = {
#                 "STATUS": "PREGAME",
#                 "DATA":"", 
#                 "MSG":"Waiting for other players..."
#             }
#             conn.sendall(json.dumps(info, indent = 4).encode())
    
#         connections.append(conn)


# def start_server(game):
#     connections = []
#     for i in range(game.player_count):
#         handle_player(connections, i)
#     return connections

# if __name__ == '__main__':
#     game = Game(1)
#     asyncio.run(start_server(game))
#     # connections = 
#     while True:
#         for connect in connections:
#             data = connect.recv(1024).decode()
#             print(f"Player 1: {data}")

# import socket


# # Player 1 setup
# PORT = 3000       # Choose a port number


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player1_socket:
#     player1_socket.bind(('0.0.0.0', PORT))
#     player1_socket.listen()


#     print(f"Player 1 listening on port {PORT}")


#    # Accept connection from Player 1
#     conn1, addr1 = player1_socket.accept()
#     with conn1:
#         print(f"Player 1 connected by {addr1}")

#         while True:
#             # Player 1 receives data
#             data1 = conn1.recv(4096).decode()
#             if not data1:
#                 break

#             info = {
#                 "STATUS": "PREGAME",
#                 "DATA":"", 
#                 "MSG":"Waiting for other players..."
#             }
#             conn1.sendall(json.dumps(info).encode())
                
#             print(f"Player 1: {data1}")
               
               
import socket
import json
import asyncio

class Game:
    def __init__(self, player_count, scoreboard):
        self.player_count: int = player_count
        self.scoreboard: list(int) = scoreboard
        
async def handle_client(reader, writer, client_id, turn_user):
    while True:
        try:
            # Read data from the client
            data = await reader.read(100)
            if not data:
                print(f"Client {client_id} disconnected.")
                break

            # Decode the received data
            message = data.decode()
            print(f"Received from Client {client_id}: {message}")

            info = {
                "STATUS": "PREGAME",
                "DATA":"", 
                "MSG":"Waiting for other players..."
            }

            # Respond to the client
            writer.write(json.dumps(info, indent = 4).encode())
            await writer.drain()
            
        except asyncio.CancelledError:
            print("Cancelled event")
            break
        
        except Exception as e:
            print(f"Error handling client {client_id}: {e}")
            break
    writer.close()

async def start_server(game):
    host = '0.0.0.0'
    port_base = 3000
    client_id = 0
    turn = 1

    async def on_client_connected(reader, writer):
        nonlocal client_id
        client_id += 1
        print(f"Accepted connection from {writer.get_extra_info('peername')}")
        await handle_client(reader, writer, client_id, turn)
        
    server = await asyncio.start_server(on_client_connected, host, port_base)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    game = Game(2)
    asyncio.run(start_server(game))