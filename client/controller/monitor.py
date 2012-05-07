import os 
import copy
import action
import time

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
        self.old_files = copy.copy(self.files)
        
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
    
class ProcMonitor:
    def __init__(self, application, max_ptime=3):
        """
        @param application: Application being fuzzed that needs to be monitored
        @param max_ptime: Maximum amount of time a processes should be running.
                          If process exceeds this time it will be killed 
        """
        self.application = application
        self.max_ptime = max_ptime
        self.action = action.Action()
        self.process_ids = {}
        
    def watch_fuzzed_app(self):
        """
        Watch for application that enters infinite loop or cpu exhaustion state. 
        If an app has been running for too long then kill it 
        """
        while(True):
            time.sleep(self.max_ptime)
            cmd = "ps -A | grep " + str(self.application) 
            ps = self.action.run(cmd)
            if ps: 
                #get process id 
                proc_id = ps[0].split(" ")[0].strip()
                if self.process_ids.get(proc_id):
                    k_cmd = "kill -9 " + proc_id
                    self.action.run(k_cmd)
                else:
                    self.process_ids[proc_id] = proc_id
            
if __name__ == "__main__":
    m = DirectoryMonitor("./")
    print m.get_new_files()
    print m.files
    print m.get_core_files()
    print m.get_new_core_files()
    
    p = ProcMonitor("sleep")
    p.watch_fuzzed_app()
    