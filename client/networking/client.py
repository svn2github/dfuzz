import socket
import sys
import md5
import random

SERVER, PORT = "192.160.0.140", 12456

if 1:
    rand = random.randint(1000000,9999999)
    hash = md5.new(str(rand))
    data = "10001|"+hash.hexdigest()+"|test"+str(rand)+".pdf"

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server and send data
        print "Sending : "+data
        print "to "+SERVER+":"+str(PORT)+"\n"
        sock.connect((SERVER, PORT))
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        #received = sock.recv(1024)
    finally:
        sock.close()
