import json
from typing import List
from typing import Optional

def encode_client_data(status: str, dice:Optional[List[int]]=None, fixed_index:Optional[List[int]]=None, score:Optional[int]=None,  score_index:Optional[int]=None, remaining_roll:Optional[int]=None):
    data = {}
    
    match status:
        case "ROLL":
            data['dice'] = dice
            data['fixed_index'] = fixed_index
            data['remaining_roll'] = remaining_roll
        case "END_TURN":
            data["score"]=score
            data["score_index"]=score_index
        
    packet = {"status":status, "data":data}
    
    print(f'----- CLIENT -> SERVER -----\npacket\n')
    
    json_data = json.dumps(packet, indent = 4)
    
    return json_data.encode()

def encode_server_data(status: str, remaining_roll:Optional[int]=None, dice:Optional[list[int]]=None, fixed_index:Optional[list[bool]]=None):
    data = {}
    msg = None
    
    match status:
        case "PREGAME":
            print('testing...')
            msg = "Waiting for other players..."
        case "TURN":
            data["remaining_roll"]=remaining_roll
            data["dice"]=dice
            data['fixed_index']=fixed_index
            msg = f"You have {remaining_roll} remaining"
        case "WAIT":
            print(f'received {remaining_roll} {dice}')
            data["remaining_roll"]=remaining_roll
            data["dice"]=dice
            msg = f"Currently opponent's roll"
        case "END":
            msg = "You won!"
        
    packet = {"status":status, "data":data, "msg":msg}
    
    print(f'----- SERVER -> CLIENT -----\npacket\n')

    json_data = json.dumps(packet, indent = 4)
    return json_data.encode()

def decode_server_data(byte_data):
    str_data = byte_data.decode()
    return json.loads(str_data)

def decode_client_data(byte_data):
    str_data = byte_data.decode()
    res = json.loads(str_data)
    return res