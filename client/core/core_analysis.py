#!/usr/bin/env python

import os
import subprocess 
import glob
import time 

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
        self.gdb = subprocess.Popen(['gdb'], bufsize=LINE_BUFFERED, stdin=subprocess.PIPE)
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
    
    def stop_gdb(self):
        self.gdb.close()    
        
        
if __name__ == "__main__":
    c = Core()
    c.start_gdb()
    c.set_program("/usr/bin/pdftotext")
    c.set_core_file("core.11203")
    output = c.get_backtrace()
    print "!!!!!!!!!!!!!!!!!!!!BACKTRACE!!!!!!!!!!!!!!"
    print output