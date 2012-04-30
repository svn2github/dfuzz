import os
import sys
import inspect

class Config():
    def __init__(self):
        """
        initialize configuration variables and parsing parameters
        """
        self.config = {}
        self.config_dir = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe()))) # script directory
        self.config_file = os.path.abspath(os.path.join(self.config_dir, "dfuzz.config"))
        self.results_dir = os.path.abspath(os.path.join(self.config_dir, "../results"))
        self.config_declaration_sep = "==="
        self.config_separator = '"""'
        self.supported_configurations = {"fuzzing_prog": True,
                                    "fuzzing_prog_folder": True,
                                    "fuzzing_prog_args": True,
                                    "users": True,
                                    "mutation_folder": True
                                    }
    
    def parse(self):
        """
        parse configuration file and store configurations in self.config
        """
        fh = open(self.config_file, "r")
        for line in fh:
            c = line.split(self.config_declaration_sep)
            if c and len(c) > 1:
                key = c[0].strip()
                if self.supported_configurations.get(key):
                    value = c[1].strip().split(self.config_separator)[1]
                    self.config[key] = value
                    
                    
if __name__ == "__main__":
    c = Config()
    c.parse()
    print c.config
                
                