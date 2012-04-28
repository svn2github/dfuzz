#!/usr/bin/env python

import os
import subprocess 
import glob

bt_dict = {}
fh = open("gdb_cmds", "w")
fh.write("bt\n")
fh.write("quit\n")
fh.close()
core_files = glob.glob("core.*")
for core_file in core_files:
    print "processing " + core_file
    backtrace = ""
    cmd = 'gdb -x "gdb_cmds" -q pdftotext ' + core_file + '| grep "\#"'  
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
    tmp = str.split(p, "\n")
    for line in tmp: 
        if len(str.split(line, " in ")) >= 2:
            backtrace = backtrace + str.split(line, " in ")[1]
    
    bt_dict[backtrace] = core_file
print "unique core dumps"
print len(bt_dict)
