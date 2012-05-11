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
import core_processor


class Controller():
    def __init__(self):
        self.config = config.Config()
        self.config.parse()
        self.core_p = core_processor.ProcessCores()
    
    def start(self):
        _action = action.Action()
        #turn on core dumps
        #max size of 22000 blocks (guessing that is 22 megabytes on typical linux system)
        _action.run("ulimit -c 22000")
        trunk = os.path.join(cwd, "../../")
        os.chdir(os.path.join(trunk,self.config.config["fuzzing_prog_folder"]))
        fuzz_prog = os.path.split(self.config.config["fuzzing_prog"])[1]
        fuzz_cmd = "./" + fuzz_prog +" " + self.config.config["fuzzing_prog_args"]
        os.system(fuzz_cmd)
    
    def start_monitor(self):
        """
        start monitoring a directory and reporting results
        """
        results_dir = os.path.join(cwd,"../results")
        dm = monitor.DirectoryMonitor(results_dir)
        pm = monitor.ProcMonitor(self.config.config["fuzzed_program_name"])
        _core_processer = core_processor.ProcessCores()
        while 1:
            pm.watch_fuzzed_app()
            new_files = dm.get_new_files()
            if new_files:
                self.core_p.process_core_bts()
                self.core_p.report_results(new_files)
            time.sleep(4)
            
if __name__ == "__main__":
    c = Controller()
    if len(sys.argv) > 1:
        c.start_monitor()
    else:
        c.start()