import os
import sys
import unittest
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../networking/"))
import sftp

class Test(unittest.TestCase):

    def setUp(self):
        self.sftp = sftp.SFTP()
        
    def testName(self):
        host = "192.168.1.89"
        local_file = "test.txt"
        remote_file = "/root/test.txt"
        self.sftp.put(host, "root", local_file, remote_file)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    