import base64

class Utils:    

    def create_datagram_message(drone_id, msg_body):
        return drone_id.encode() + base64.b64encode(msg_body)   

    # def readNetworkMessage(socket):
        
    #     body_size = int.from_bytes(socket.recv(4), byteorder='big')
    #     body = socket.recv(body_size)
        
    #     return body
        
        
    # def createNetworkMessage(msg_body_bytes):
        
    #     length = len(msg_body_bytes)
    #     length_encoded_to_4_bytes = (length).to_bytes(4, byteorder='big')
        
    #     return length_encoded_to_4_bytes + msg_body_bytes 