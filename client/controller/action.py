import os

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

if __name__ == "__main__":
    a = Action()
    a.run_as("user_name", "whoami")