import os
import sys
import unittest
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../config/"))
import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        """
        Initalize configuration object
        """
        self.config = config.Config()

    def test_parse(self):
        """
        Test that configuration parse function works and 
        that a class variable config is initalized
        """
        self.config.parse()
        self.assertTrue(self.config.config)
    
    def test_get_dfuzz_id(self):
        """
        Test that the dfuzz id that is returned has a type of str (string)
        """
        self.config.parse()
        dfuzz_id = self.config.get_dfuzz_id()
        self.assertTrue(type(dfuzz_id)==type(""))
        
if __name__ == '__main__':
    unittest.main()