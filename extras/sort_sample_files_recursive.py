import fnmatch
import os
import operator
import shutil


if __name__ == "__main__":
    matches = []
    for root, dirnames, filenames in os.walk('/home/user/pdf_harvestfest/'):
      for filename in fnmatch.filter(filenames, '*.pdf'):
          matches.append(os.path.join(root, filename))
    
    for i in xrange(len(matches)):
        statinfo = os.stat(matches[i])
        matches[i] = matches[i],statinfo.st_size,statinfo.st_ctime
    
    matches.sort(key=operator.itemgetter(1))
    #print 'sorted by size:',matches
    
    print "LENGTH ", len(matches) 
    print matches[0][0]
    folder_name = 1
    os.mkdir(str(folder_name))
    for i in xrange(len(matches)):
        if i % 10000 == 0:
            folder_name = folder_name + 1
            os.mkdir(str(folder_name))
        
        f_name = str(folder_name)
        cwd = os.path.curdir
        shutil.move(matches[i][0] , os.path.abspath(os.path.join(cwd, f_name)))   
        
            
        
      