import socket
import sys
import random


class Client():
    def __init__(self, server="192.168.1.78", port=12456):
        """
        @param server: IP address of server that we need to connect to 
        @param port: port that we need to connect to (typically tcp port 12456) 
        """
        self.server = server
        self.port = port
        
    
    def send(self, data):
        """
        @param data: data that will be sent to the server
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            sock.connect((self.server, self.port))
            sock.sendall(data)
    
            # Receive data from the server and shut down
            #received = sock.recv(1024)
        finally:
            sock.close()
        
   
if __name__ == "__main__":
    c = Client("192.168.1.78", 12456)
    
    #generate rand string to send over the wire
    rand = random.randint(1000000,9999999)
    hash = "12121235577"
    data = "10001|"+hash.hexdigest()+"|test"+str(rand)+".pdf" + "|" + "123808"
    
    #send data
    c.send(data)    
#