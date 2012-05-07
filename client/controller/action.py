import os
import time
import signal
import subprocess

class Action():
    """
    This class can be used to execute operations on the client
    """
    def run_as(self, username, cmd):
        """
        Execute a command as a user
        @param username: The user the command should be run under
        @param cmd: Command to be executed
        """
        pipe = os.popen("su %s" % username, 'w')
        pipe.write(cmd)

    def run_timed(self, cmd, seconds=3):
        """
        Run a command that willl be killed in a certain amount of time
        @param cmd: Command that will be executed
        @param seconds: seconds to wait before the program is killed
        """
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(seconds)
        if pipe:
            pipe.kill()
        
    def run_timed2(self, cmd, seconds=3):
        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        time.sleep(seconds)
        os.killpg(pro.pid, signal.SIGTERM)
        
    def run(self, cmd):
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return pipe.communicate()   
        
if __name__ == "__main__":
    a = Action()
    p = a.run_timed("evince")