import os
import sys
import inspect
cwd = os.path.split(os.path.realpath(__file__))[0]

class Config():
    def __init__(self):
        """
        initialize configuration variables and parsing parameters
        """
        self.__dfuzz_id = None
        
        self.config = {}
        self.config_dir = cwd
        self.dfuzz_id_file = os.path.abspath(os.path.join(self.config_dir, "dfuzz.id"))
        self.config_file = os.path.abspath(os.path.join(self.config_dir, "dfuzz.config"))
        self.results_dir = os.path.abspath(os.path.join(self.config_dir, "../results"))
        self.config_declaration_sep = "==="
        self.config_separator = '"""'
        self.supported_configurations = {"fuzzing_prog": True,
                                    "fuzzing_prog_folder": True,
                                    "fuzzing_prog_args": True,
                                    "users": True,
                                    "mutation_folder": True,
                                    "fuzzed_program": True,
                                    "fuzzed_program_name": True
                                    }
        
        self.supported_id_configurations = {"dfuzz_id": True}
        
    
    def parse(self):
        """
        parse configuration file and store configurations in self.config
        """
        #parse configuration file
        fh = open(self.config_file, "r")
        for line in fh:
            c = line.split(self.config_declaration_sep)
            if c and len(c) > 1:
                key = c[0].strip()
                if self.supported_configurations.get(key):
                    value = c[1].strip().split(self.config_separator)[1]
                    self.config[key] = value
        
        #parse dfuzz id
        fh_id = open(self.dfuzz_id_file)
        for line in fh_id:
            c = line.split(self.config_declaration_sep)
            if c and len(c) > 1:
                key = c[0].strip()
                if self.supported_id_configurations.get(key):
                    value = c[1].strip().split(self.config_separator)[1]
                    self.__dfuzz_id = value
        
    def get_dfuzz_id(self):
        """
        @return: dfuzz unique identification
        """
        return self.__dfuzz_id        
        
if __name__ == "__main__":
    c = Config()
    c.parse()
    print c.config
    print c.get_dfuzz_id()
                
                