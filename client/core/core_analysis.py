#!/usr/bin/env python

import os
import subprocess 
import time 
import hashlib
import re
import glob
import sys
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../config/"))
import config

LINE_BUFFERED = 1

class CoreGDB():
    
    def __init__(self):
        self.config = config.Config()
        self.config.parse()
        self.unique_cores = []
        self.unique_core_dic = {}
    
    def start_gdb(self):
        """
        initalize gdb and return a process handle to the program
        """
        #self.gdb = subprocess.Popen(['gdb'], bufsize=LINE_BUFFERED, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        self.gdb = subprocess.Popen(['gdb'], stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        time.sleep(1) 
            
    def set_core_file(self, core_file):
        """
        load core file in gdb
        @param core_file: core dump file to be processed by gdb
        """
        if self.gdb:
            self.gdb.stdin.write("core-file %s\n" %core_file)    
    
    def unset_environment(self):
        """
        clear all environment variables
        """
        if self.gdb:
            self.gdb.stdin.write("unset environment\n")
            self.gdb.stdin.write("y\n")
        
    def set_program(self, program):
        """
        @param program: executable that crashed and in turn 
                        caused the operating system to produce a core file
        """
        if self.gdb:
            self.gdb.stdin.write("file %s\n" %program)
    
    def get_backtrace(self, length=10):
        """
        @param length: length of backtrace 
        """
        if self.gdb:
            self.gdb.stdin.write("bt %s\n" %str(length))
        time.sleep(2)
        return self.gdb.communicate()[0]
    
    def get_frame_trace(self, length=10):
        """
        @param length: length of frame trace
        """
        frame_trace = ""
        frame_count = 0
        self.gdb.stdin.write("frame \n")
        line_in = self.gdb.stdout.readline()
        while ((not "you cannot go up" in line_in) and frame_count < 70):
            line_in = self.gdb.stdout.readline()
            frame_trace = frame_trace + str(line_in)
            self.gdb.stdin.write("up \n")
            frame_count = frame_count + 1
        return frame_trace
   
    def get_unique_cores(self, directory):
        """
        @param directory: directory where core files exist
        """
        self.unique_cores = []
        for core_file in glob.glob(os.path.join(directory,"core.*")):
            self.stop_gdb()
            self.start_gdb()
            self.set_program(self.config.config["fuzzed_program"])
            self.set_core_file(core_file)
            frame_trace = self.get_frame_trace()
            crash_hash = self.get_unique_crash_hash(frame_trace)
            if not self.unique_core_dic.get(crash_hash):
                self.unique_core_dic[crash_hash] = core_file
                self.unique_cores.append(core_file)
        return self.unique_cores
    
    def get_cores(self, directory):
        return glob.glob(os.path.join(directory,"core.*"))
            
    #reverse backtrace  (show reverse-backtrace)
    
    def gdb_is_alive(self):
        """
        Check to see if a gdb instance exists
        @return: True if it is alive and False if a gdb instance does not exist
        """
        try:
            _alive = False
            if self.gdb:
                _alive = True 
            return _alive
        except:
            return False
    
    def stop_gdb(self):
        """
        kill gdb
        """
        if self.gdb:
            self.gdb.kill()    
        
    def get_unique_crash_hash(self, backtrace):
        """
        @param backtrace: the functions and addresses that are displayed in GDB 
        when issuing the command 'bt'. 
        """
        bt = ""
        pattern = re.compile(r"[\(gdb\)]*\s*#[0-9]+\s+0x[a-zA-Z0-9_]+\s+in")
        backtrace = backtrace.split('\n')
        for line in backtrace:
            if pattern.match(line):
                #assumes debugging symbols (gets function names of backtrace)
                bt = bt + line.split(" in ")[1].split("()")[0].strip() 
        crash_hash = hashlib.sha1(bt)
        return crash_hash.hexdigest()

class CoreFileSize():
    
    def __init__(self):
        """
        initialize unique core variables
        """
        self.unique_cores = []
        self.unique_core_dic = {}
        
    def get_unique_cores(self, directory):
        """
        Calculate unique core files based on file size. Files are measured in kilibytes
        @return: list of unique core files 
        @rtype: array
        """
        self.unique_cores = []
        for core_file in glob.glob(os.path.join(directory,"core.*")): 
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(core_file)
            kb = size/1024
            if not self.unique_core_dic.get(kb):
                self.unique_core_dic[kb] = core_file
                self.unique_cores.append(core_file)
        return self.unique_cores
            

class Crash():
    
    def __init__(self):
        """
        Initialize configuration
        """
        self.config = config.Config()
        self.config.parse()
        self.fuzz_prog = self.config.config["fuzzed_program_name"]
    
    def get_file_that_cause_crash(self, core_file, mutation_dir):
        """
        @param core_file: core dump file 
        @param mutation_dir: directory where mutated/generated files are loaded into the fuzzed program
        @return: return the name of the file that caused the crash 
        """
        min_len = str(len(mutation_dir) - 3)
        cmd = 'strings -n ' + min_len + ' ' + core_file + '| grep "' + mutation_dir + '" | grep "\.pdf" | grep -v ' + self.fuzz_prog + ' | head -1'
        crash_file = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
        return str(crash_file).strip()
    
    def compute_sha1_hash_of_file(self, file):
        """
        compute the sha1 sum of a file
        @param file: file to hash
        @return: Hex representation of message digest (hash) of file
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
    boo = CoreFileSize()
    print boo.get_unique_cores("/home/username/workspace/dfuzz/trunk/fuzzing_applications/filep/")
    c1 = Crash()
    print c1.get_file_that_cause_crash("core.11203", "fuzzing_applications/filep/out")
    print c1.compute_sha1_hash_of_file("core.11203")
    print c1.compute_sha256_hash_of_file("core.11203")
    c = CoreGDB()
    #c.start_gdb()
    #c.set_program("/usr/bin/pdftotext")
#    for file in glob.glob("/home/username/workspace/dfuzz/trunk/fuzzing_applications/filep/core.*"):
#        c.start_gdb()
#        c.set_program("/usr/bin/pdftotext")
#        c.set_core_file(file)
#        output = c.get_backtrace()
#        print "!!!!!!!!!!!!!!!!!!!!BACKTRACE!!!!!!!!!!!!!!"
#        print output
#        print c.get_unique_crash_hash(output)