import socket
import sys
import md5
import random


class Client():
    def __init__(self, server, port):
        self.server = server
        self.port = port
        
    
    def send(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            print "Sending : "+data
            print "to "+self.server+":"+str(self.port)+"\n"
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
    hash = md5.new(str(rand))
    data = "10001|"+hash.hexdigest()+"|test"+str(rand)+".pdf" + "|" + "123808"
    
    #send data
    c.send(data)    
#