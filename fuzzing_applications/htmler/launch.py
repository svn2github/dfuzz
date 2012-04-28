#!/usr/bin/env python 

import os 
import time
files = os.listdir("./html1")
for file in files: 
   cmd = "firefox ./html1/"+ file + " &"
   os.system(cmd)
   time.sleep(5)
   os.system("killall firefox")
   
