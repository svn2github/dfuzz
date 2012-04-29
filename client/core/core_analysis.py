#!/usr/bin/env python

import os
import subprocess 
import time 
import hashlib

#bt_dict = {}
#fh = open("gdb_cmds", "w")
#fh.write("bt\n")
#fh.write("quit\n")
#fh.close()
#core_files = glob.glob("core.*")
#for core_file in core_files:
#    print "processing " + core_file
#    backtrace = ""
#    cmd = 'gdb -x "gdb_cmds" -q pdftotext ' + core_file + '| grep "\#"'  
#    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
#    tmp = str.split(p, "\n")
#    for line in tmp: 
#        if len(str.split(line, " in ")) >= 2:
#            backtrace = backtrace + str.split(line, " in ")[1]
#    
#    bt_dict[backtrace] = core_file
#print "unique core dumps"
#print len(bt_dict)


LINE_BUFFERED = 1

class Core():
    def start_gdb(self):
        self.gdb = subprocess.Popen(['gdb'], bufsize=LINE_BUFFERED, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(1)
        return self.gdb 
            
    def set_core_file(self, core_file):
        """
        load core file in gdb
        """
        if self.gdb:
            self.gdb.stdin.write("core-file %s\n" %core_file)    
    
    def unset_environment(self):
        if self.gdb:
            self.gdb.stdin.write("unset environment\n")
            self.gdb.stdin.write("y\n")
        
    def set_program(self, program):
        if self.gdb:
            self.gdb.stdin.write("file %s\n" %program)
    
    def get_backtrace(self):
        if self.gdb:
            self.gdb.stdin.write("bt 10\n")
        out, err = self.gdb.communicate()
        return out
    
    #reverse backtrace  (show reverse-backtrace)
    
    def stop_gdb(self):
        self.gdb.kill()    
        
    def get_unique_crash_hash(self, backtrace):
        crash_hash = hashlib.sha1(backtrace)
        return crash_hash.hexdigest()

class Crash():

    def get_file_that_cause_crash(self, core_file, mutation_dir):
        min_len = str(len(mutation_dir) - 3)
        cmd = 'strings -n ' + min_len + ' ' + core_file + '| grep "' + mutation_dir + '" | grep pdf | head -1'
        crash_file = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
        return crash_file
    
    def compute_sha1_hash_of_file(self, file):
        """
        compute the sha1 sum of a file
        """
        sha1_hash = hashlib.sha1()
        file_handle = open(file, "rb")
        #read 16M at a time (this will prevent against memory exhaustion)
        data = file_handle.read(16 * 1024 * 1024)
        sha1_hash.update(data)
        file_handle.close()
        return sha1_hash.hexdigest()
    
    def compute_sha256_hash_of_file(self, file):
        """
        compute the sha2 sum of a file
        @param file: file to hash
        @return: Hex representation of message digest (hash) of file
        """
        sha256_hash = hashlib.sha256()
        file_handle = open(file, "rb")
        #read 16M at a time (this will prevent against memory exhaustion)
        data = file_handle.read(16 * 1024 * 1024)
        sha256_hash.update(data)
        file_handle.close()
        return sha256_hash.hexdigest()

        
if __name__ == "__main__":
    c1 = Crash()
    print c1.get_file_that_cause_crash("core.11203", "fuzzing_applications/filep/out")
    print c1.compute_sha1_hash_of_file("core.11203")
    print c1.compute_sha256_hash_of_file("core.11203")
    c = Core()
    c.start_gdb()
    c.set_program("/usr/bin/pdftotext")
    c.set_core_file("core.11203")
    output = c.get_backtrace()
    print "!!!!!!!!!!!!!!!!!!!!BACKTRACE!!!!!!!!!!!!!!"
    print output
    print c.get_unique_crash_hash(output)