#!/usr/bin/env python

import os
import sys
import subprocess
import action
cwd = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(cwd, "../config/"))
sys.path.append(os.path.join(cwd, "../core/"))
import config
import core_processer

class Controller():
    def __init__(self):
        self.config = config.Config()
        self.config.parse()
    
    def start(self):
        _action = action.Action()
        #turn on core dumps
        _action.run("ulimit -c unlimited")
        trunk = os.path.join(cwd, "../../")
        os.chdir(os.path.join(trunk,self.config.config["fuzzing_prog_folder"]))
        fuzz_prog = os.path.split(self.config.config["fuzzing_prog"])[1]
        fuzz_cmd = "./" + fuzz_prog +" " + self.config.config["fuzzing_prog_args"]
        os.system(fuzz_cmd)
        
if __name__ == "__main__":
    c = Controller()
    c.start()