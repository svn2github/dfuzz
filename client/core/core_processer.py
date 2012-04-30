import os
import core_analysis
import sys
import shutil
sys.path.append("../config/")
import config


class ProcessCores():
    def __init__(self):
        """
        initialize configuration and other helper classes
        """
        self.cfsize = core_analysis.CoreFileSize()
        self.config = config.Config()
        self.crash = core_analysis.Crash()
        self.config.parse()
        self.mutation_folder = os.path.abspath(os.path.join("../../",self.config.config["mutation_folder"]))
        
        
    def process_cores(self):
        print "processing cores"
        print self.config.config
        fuzz_prog_folder = os.path.abspath(os.path.join("../../", self.config.config["fuzzing_prog_folder"]))
        unique_cores = self.cfsize.get_unique_cores(fuzz_prog_folder)
        for unique_core in unique_cores:
            shutil.copy(unique_core, self.config.results_dir)
            crash_file = self.crash.get_file_that_cause_crash(unique_core, self.mutation_folder)
            shutil.copy(crash_file, self.config.results_dir)
        
if __name__ == "__main__":
    p = ProcessCores()
    p.process_cores()        