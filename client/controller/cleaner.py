import os
import glob

class Clean():
    def remove_cores(self, directory):
        """
        remove core files in a directory
        @param directory: directory in which all core files should be removed
        """
        for file in os.listdir(directory):
            if file.startswith("core."):
                os.remove(os.path.join(directory, file)) 
    
    def remove_mutation_files(self, directory, filetype):
        """
        @param directory: directory where files are located
        @param filetype: type of files that will be removed (ie. pdf, doc)
        """
        for file in os.listdir(directory):
            if file.endswith("."+filetype):
                os.remove(os.path.join(directory, file)) 