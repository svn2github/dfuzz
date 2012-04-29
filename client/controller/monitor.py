import os 

class DirectoryMonitor:
    def __init__(self, directory):
        """
        @param directory: directory that will be monitored
        """
        self.directory = directory
        self.files = {}
        self.old_files = {}
        self.new_files = []
    
    def scan(self):
        """
        Get information about a directory (eg. new files placed in the directory). 
        """
        self.new_files = []
        files = os.listdir(self.directory)
        for file in files: 
            self.files[file] = True
        for f in self.files:
            if not self.old_files.get(f):
                self.new_files.append(f)
        self.old_files = self.files
        
    def get_new_files(self):
        """
        @return: new files in a direcotry
        """
        self.scan()
        return self.new_files
    
    def get_core_files(self):
        """
        @return: a list of core files that exist in the directory
        """
        core_files = []
        self.scan()
        for file in self.files:
            if "core" in str(file):
                core_files.append(file)
        return core_files
    
    def get_new_core_files(self):
        """
        @return: core files that 
        """
        core_files = []
        self.scan()
        for file in self.new_files:
            if str(file).startswith("core."):
                core_files.append(file)
        return core_files
    
if __name__ == "__main__":
    m = DirectoryMonitor("./")
    print m.get_new_files()
    print m.files
    print m.get_core_files()
    print m.get_new_core_files()