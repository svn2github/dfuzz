import os
import sys
import unittest
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../controller/"))
import monitor

class TestMonitor(unittest.TestCase):

    def setUp(self):
        """
        Initialize directory monitor object
        """
        self.core_dir = os.path.join(cwd, "cores")
        self.directory_monitor = monitor.DirectoryMonitor(self.core_dir)
    
    def tearDown(self):
        core_1348 = os.path.join(self.core_dir, "core.1348")
        if os.path.exists(core_1348):
            os.remove(core_1348)

    def test_new_files(self):
        """
        Test that directory monitor can detect files in a directory
        """
        new_files = self.directory_monitor.get_new_files()
        self.assertTrue("core.1345" in new_files)
        self.assertTrue("core.1346" in new_files)

    def test_new_file_after_file_added(self):
        new_files = self.directory_monitor.get_new_files()
        core_1348 = os.path.join(self.core_dir, "core.1348")
        cfh = open(core_1348, "w")
        cfh.write("test")
        cfh.close()
        new_files = self.directory_monitor.get_new_files()
        self.assertTrue(new_files == ["core.1348"])
        
        
if __name__ == '__main__':
    unittest.main()