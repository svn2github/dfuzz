import MySQLdb
import SocketServer
import threading
import sftp
import os

class FuzzServer(SocketServer.BaseRequestHandler):    

    def handle(self):
        print "Receiving data from "+self.client_address[0]
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()	
        # tokenize received data
        print "Received "+self.data
        import pdb;pdb.set_trace()
        self.tokenize_protocol(self.data)
        if self.message_type == "40":
            self.retreive_crash_file()
        
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
        
    def tokenize_protocol(self, data):
        print "tokenizing protocol"
        self.values = self.data.split("|")
        self.message_type = self.values[0]
        self.hostid = self.values[1]
        self.bthash = self.values[2]
        self.filename = self.values[3]
            
    def retreive_crash_file(self):
        self.sftp = sftp.SFTP()
        if not os.path.exists("loot"):
            os.mkdir("loot")
        host = self.client_address[0]
        username = "root"
        filename = os.path.split(self.filename)[1]
        local_file = os.path.join("loot", filename)
        remote_file = self.filename
        self.sftp.get(host, username, local_file, remote_file)
        self.sftp = None
        
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
    
    
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 12456

    # Create the server, binding to localhost on port 12456
    print "Opening port %i." % PORT
    server = ThreadedTCPServer((HOST, PORT), FuzzServer)

    # create local db connection
    # front end server maintains constant db connection since it is the only 'user'		    	
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    
    





 




