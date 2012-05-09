import os
import sys
import unittest
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../core/"))
import core_analysis

class TestCoreGDB(unittest.TestCase):
    
    def setUp(self):
        """
        Initalize core processor object
        """
        self.core_gdb = core_analysis.CoreGDB()
        
    def test_core(self):
        self.core_gdb.start_gdb()
        self.assertTrue(self.core_gdb.gdb)