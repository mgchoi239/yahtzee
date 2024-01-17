import json
import asyncio
import base64


class Game:
    def __init__(self, player_count):
        self.player_count: int = player_count
        self.curr_player: int = 0
        self.scoreboard: list(int) = [[0]*12 for _ in range(player_count)]
        self.turn = 1

async def turn(writer, reader, message):
    print(message)
    writer.write(message.encode())
    await writer.drain()
    print("SENT " + message)
    
    data = await reader.read(100)
    new_message = data.decode()
    print("RECEIVED " + new_message)
    
    writer.close()
    await writer.wait_closed()
    
    return new_message
      
async def handle_client(reader, writer, client_id):
    info = {
        "STATUS": "PREGAME",
        "DATA":"", 
        "MSG":"Waiting for other players"
    }
    
    msg = await turn(reader, writer, json.dumps(info))
    print("SENT PREGAME to " + str(client_id))
    return msg

# async def play_game():
    try:
        while True:
            for i in range(1, game.player_count+1):
                if i == game.turn:
                    info = {
                        "STATUS": "TURN",
                        "DATA":{"remaining_roll":3, "dice":[1,2,3,4,5,5]}, 
                        "MSG":"Your turn!"
                    }
                else:
                    info = {
                        "STATUS": "WAIT",
                        "DATA":"", 
                        "MSG":"Currently player {}'s turn...".format(i)
                    }
                await send_message(writer, info)
                print(f'message to player {i} sent')
    except asyncio.CancelledError:
        print("Cancelled event")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def start_game_server(game):
    host = '0.0.0.0'
    port_base = 3000
    client_id = 0

    async def on_client_connected(reader, writer):
        nonlocal client_id
        client_id += 1
        # print(client_id)
        # msg = await handle_client(reader, writer, client_id)
        # print("RECEIVED BACK : " + msg)
        
        data = await reader.read(100)
        message = data.decode()
        print(f"Accepted connection from {writer.get_extra_info('peername')}")

        info = {
            "STATUS": "PREGAME",
            "DATA":"", 
            "MSG":"Waiting for other players"
        }

        msg = json.dumps(info)

        writer.write(msg.encode())
        await writer.drain()

        print("SENT " + msg)
        
        writer.close()
        await writer.wait_closed()
        
        # if client_id == game.player_count:
        #     async with game_started_condition:
        #         game_started_condition.notify_all()
        #         for writer in writers:
        #             info = {
        #                 "STATUS": "TURN",
        #                 "DATA":"", 
        #                 "MSG":"Waiting for other players"
        #             }
        #             await send_message(writer, info)
        #             print('sent message ' + str(info))
        #     await play_game()
            
        #     print("passed")
        #     for i in range(1, game.player_count+1):
        #         if i == game.turn:
        #             info = {
        #                 "STATUS": "TURN",
        #                 "DATA":{"remaining_roll":3, "dice":[1,2,3,4,5,5]}, 
        #                 "MSG":"Your turn!"
        #             }
        #         else:
        #             info = {
        #                 "STATUS": "WAIT",
        #                 "DATA":"", 
        #                 "MSG":"Currently player {}'s turn...".format(i)
        #             }
        #         await send_message(writer, info)
        #         print(f'message to player {i} sent')
        
    server = await asyncio.start_server(on_client_connected, host, port_base)

    async with server:
        # Wait until the required number of clients have connected
        # async with game_started_condition:
        #     await game_started_condition.wait()
        # print("Game started!")
        await server.serve_forever()
    
if __name__ == '__main__':
    game = Game(2)
    asyncio.run(start_game_server(game))    