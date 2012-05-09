import os
import sys
import unittest
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../controller/"))
import monitor

class TestConfig(unittest.TestCase):

    def setUp(self):
        """
        Initalize directory monitor object
        """
        core_dir = os.path.join(cwd, "cores")
        self.directory_monitor = monitor.DirectoryMonitor(core_dir)

    def test_parse(self):
        """
        """
        new_files = self.directory_monitor.get_new_files()
    	self.assertTrue("core.1345" in new_files)
    	self.assertTrue("core.1346" in new_files)

if __name__ == '__main__':
    unittest.main()