#!/usr/bin/env python

import os
import sys
import action
import monitor
import time
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../config/"))
sys.path.append(os.path.join(cwd, "../core/"))
import config
import core_processer

class Controller():
    def __init__(self):
        self.config = config.Config()
        self.config.parse()
        self.core_p = core_processer.ProcessCores()
    
    def start(self):
        _action = action.Action()
        #turn on core dumps
        _action.run("ulimit -c unlimited")
        trunk = os.path.join(cwd, "../../")
        os.chdir(os.path.join(trunk,self.config.config["fuzzing_prog_folder"]))
        fuzz_prog = os.path.split(self.config.config["fuzzing_prog"])[1]
        fuzz_cmd = "./" + fuzz_prog +" " + self.config.config["fuzzing_prog_args"]
        os.system(fuzz_cmd)
    
    def start_monitor(self):
        results_dir = os.path.join(cwd,"../results")
        m = monitor.DirectoryMonitor(results_dir)
        _core_processer = core_processer.ProcessCores()
        while 1:
            new_files = m.get_new_files()
            print new_files
            if new_files:
                self.core_p.process_core_bts()
            time.sleep(5)
            
if __name__ == "__main__":
    c = Controller()
    if len(sys.argv) > 1:
        c.start_monitor()
    else:
        c.start()