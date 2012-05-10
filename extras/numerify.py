import os
import sys
files2 = os.listdir(sys.argv[1])
#files2 = sorted(files2,key=int)a
d = {}
for file in files2: 
   d[file] = file 
counter = int(sys.argv[2])
for file in files2:
   while(d.get(str(counter)+".pdf")):
      counter = counter + 1 
   os.rename(sys.argv[1]+file,sys.argv[1]+str(counter)+".pdf")
   counter = counter + 1

