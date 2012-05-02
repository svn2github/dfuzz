import MySQLdb
import SocketServer

class FuzzServer(SocketServer.BaseRequestHandler):

    def handle(self):
        print "Receiving data from "+self.client_address[0]
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()	
        # tokenize received data
        print "Received "+self.data
        self.values = self.data.split("|")
        self.hostid = self.values[0]
        self.bthash = self.values[1]
        self.filename = self.values[2]
        
        
        
        print "Making a connection to MySQL database"
        self.dbconnection = MySQLdb.connect(host="localhost",port=3306,user="dfuzz",passwd="jereSILV0406!(&*",db="DFUZZ") 
        print "Connected"
        
        #SQL INJECTION PREVENTION
        ################################################
        cursor = self.dbconnection.cursor()
        try:
           cursor.execute("INSERT INTO CRASHES(hostid,bthash,filename) VALUES (%s,%s,%s);", (self.hostid,self.bthash,self.filename) )
        except:
           #error occured
           pass
        ################################################
        
        self.dbconnection.close()
        print "Disconnected"
        
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 12456

    # Create the server, binding to localhost on port 12456
    print "Opening port %i." % PORT
    server = SocketServer.TCPServer((HOST, PORT), FuzzServer)

    # create local db connection
    # front end server maintains constant db connection since it is the only 'user'		    	
    
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()






 




