import socket

# Player 1 setup
PORT = 3000       # Choose a port number

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player1_socket:
    player1_socket.bind(('0.0.0.0', PORT))
    player1_socket.listen()

    print(f"Player 1 listening on port {PORT}")

    # Accept connection from Player 1
    conn1, addr1 = player1_socket.accept()
    with conn1:
        print(f"Player 1 connected by {addr1}")

        # Player 2 setup
        PORT += 1  # Increment port for Player 2
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as player2_socket:
            player2_socket.bind(('0.0.0.0', PORT))
            player2_socket.listen()

            print(f"Player 2 listening on port {PORT}")

            # Accept connection from Player 2
            conn2, addr2 = player2_socket.accept()
            with conn2:
                print(f"Player 2 connected by {addr2}")

                while True:
                    # Player 1 receives data
                    data1 = conn1.recv(1024).decode()
                    if not data1:
                        break

                    print(f"Player 1: {data1}")
                    # Process the data received from Player 1
                    # Implement your game logic here for Player 1

                    # Send response back to Player 1
                    conn1.sendall(f"Player 1: Received - {data1}".encode())

                    # Player 2 receives data
                    data2 = conn2.recv(1024).decode()
                    if not data2:
                        break

                    print(f"Player 2: {data2}")
                    # Process the data received from Player 2
                    # Implement your game logic here for Player 2

                    # Send response back to Player 2
                    conn2.sendall(f"Player 2: Received - {data2}".encode())