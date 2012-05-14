import MySQLdb
import SocketServer
import threading
#import sftp
import os
import random

class FuzzServer(SocketServer.BaseRequestHandler): 

    def handle(self):
        print "Receiving data from "+self.client_address[0]
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip() 
        # tokenize received data
        print "Received "+self.data
        #self.tokenize_protocol(self.data)
        
        self.values = self.data.split("|")
        self.hostid = self.client_address[0]
        self.bthash = self.values[1]
        self.filename = self.values[2]
        
        #if self.message_type == "40":
        #    self.retreive_crash_file()
        self.add_crash_info_to_database()
        #if self.message_type == "42":
        #    self.handle_report_ready()
        
#

    def add_crash_info_to_database(self):
        print "Making a connection to MySQL database"
        try:
            self.dbconnection = MySQLdb.connect(host="localhost", port=3306, user="dfuzz", passwd="jereSILV0406!(&*", db="DFUZZ") 
            if(self.dbconnection) : print "Connected"
            #self.dbConnection.autocommit(True);
            #SQL INJECTION PREVENTION
            ################################################
            
            self.cursor = self.dbconnection.cursor()
            self.cursor.execute("""INSERT INTO CRASHES(hostid,bthash,filename) VALUES (%s,%s,%s)""",(self.hostid, self.bthash, self.filename))            ################################################
            self.dbconnection.commit()           
        except:
            print "Connection error!"
            pass
        finally:              
            self.cursor2 = self.dbconnection.cursor() 
            self.cursor2.execute("""SELECT * FROM (SELECT bthash, COUNT(*) FROM CRASHES GROUP BY bthash) as temp WHERE bthash=%s""",(self.bthash))            
            
            self.uniqueness = self.cursor2.fetchone()            
            if(self.uniqueness) :    
                print "Number of these = "+str(self.uniqueness[1])
                if (self.uniqueness==1) : retrieve_crash_file()
            self.dbconnection.close()
            print "Disconnected"


    def tokenize_protocol(self, data):
        """
        Parse protocol and organize protocol information
        @param data: The data received from the client
        """
        print "tokenizing protocol"
        self.values = self.data.split("|")
        self.message_type = self.values[0]
        if self.message_type == "42": 
            self.first_time = self.values[1]
        else: 
            self.hostid = self.values[1]
            self.bthash = self.values[2]
            self.filename = self.values[3]

    def handle_report_ready(self):
        if self.first_time == "1":
            #get dfuzz id from database
            #setting dfuzz id to random number temporarilly
            self.dfuzz_id_counter = str(random.randint(1,500000))
            self.request.sendall(self.dfuzz_id_counter)


    def retreive_crash_file(self):
        """
        After receiving a crash message from a client this function should use 
        sftp to transfer the file that caused the crash on the client back to the server
        """
        _sftp = sftp.SFTP()
        if not os.path.exists("loot"):
            os.mkdir("loot")
        host = self.client_address[0]
        username = "root"
        filename = os.path.split(self.filename)[1]
        local_file = os.path.join("loot", filename)
        remote_file = self.filename
        _sftp.get(host, username, local_file, remote_file, "dfuzz!")
        _sftp = None

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

