import os
import paramiko
#yum install python-paramiko
#http://www.lag.net/paramiko/docs/

#ssh-keygen
#ssh-copy-id 192.168.1.90

class SFTP():
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        
    def get(self, host, username, local_file, remote_file, password=None):
        """
        @param host: IP address of host where file resides 
        @param username: username on remote machine 
        @param local_file: local location of where to download the file to 
        @param remote_file: filename to get on remote machine
        @param password: password of remote machine (keys are typically used so this will typically be None) 
        """
        self.ssh.connect(host, username=username, password=password)
        sftp = self.ssh.open_sftp()
        sftp.get(remote_file, local_file)
        sftp.close()
        self.ssh.close()

    def put(self, host, username, local_file, remote_file, password=None):
        """
        @param host: IP address of remote machine where file is to be transfered 
        @param username: username on remote machine 
        @param local_file: file that resides on local macine that is to be transfered
        @param remote_file: remote location of where file is to be transfered
        @param password: password of the remote user on the remote machine
        """
        self.ssh.connect(host, username=username, password=password)
        sftp = self.ssh.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        self.ssh.close()

if __name__ == "__main__":        
    host = "192.168.1.90"
    local_file = "test.txt"
    remote_file = "/root/test.txt"
    s = SFTP()
    s.put(host, "root", local_file, remote_file)