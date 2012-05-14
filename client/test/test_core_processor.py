import os
import sys
import unittest
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../core/"))
import core_processor

class TestCoreProcessor(unittest.TestCase):
    
    def setUp(self):
        """
        Initalize core processor object
        """
        self.core_processor = core_processor.ProcessCores()

    def test_core(self):
        self.core_processor.process_cores()
        self.core_processor.gdb.stop_gdb()

   # def test_core_bt(self):
    #    self.core_processor.process_core_bts()

if __name__ == "__main__":
    unittest.main()