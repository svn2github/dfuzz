import os
import sys
import unittest
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../core/"))
sys.path.append(os.path.join(cwd, "../config/"))
import core_analysis
import config

class TestCoreGDB(unittest.TestCase):
    
    def setUp(self):
        """
        Initalize core processor object
        """
        self.config = config.Config()
        self.config.parse()
        self.core_gdb = core_analysis.CoreGDB()
        
    def test_core(self):
        self.core_gdb.start_gdb()
        self.assertTrue(self.core_gdb.gdb)
        
    def test_frame_trace(self):
        """
        test core analysis frame tracing technique
        """
        self.core_gdb.start_gdb()
        self.core_gdb.set_program(self.config.config["fuzzed_program"])
        self.core_gdb.set_core_file("cores/core.10049")
        ft = self.core_gdb.get_frame_trace()
        self.assertTrue(ft)
    
    def test_unique_cores(self):
        """
        test core analysis unique core functionality
        """
        self.core_gdb.start_gdb()
        unique_cores = self.core_gdb.get_unique_cores("cores/")
        self.assertTrue(len(unique_cores)==2)
        
        
if __name__ == '__main__':
    unittest.main()        