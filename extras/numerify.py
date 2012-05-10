import os
import sys
#small script to rename files in a folder to use a consistent name
#python numerify.py /home/user/pdfs/ 3000000

files2 = os.listdir(sys.argv[1])
d = {}
for file in files2: 
   d[file] = file 
counter = int(sys.argv[2])
for file in files2:
   while(d.get(str(counter)+".pdf")):
      counter = counter + 1 
   os.rename(sys.argv[1]+file,sys.argv[1]+str(counter)+".pdf")
   counter = counter + 1

