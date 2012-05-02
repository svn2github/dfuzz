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
        
    def get(self, host, username, local_file, remote_file):
        self.ssh.connect(host, username="root", password=None)
        sftp = self.ssh.open_sftp()
        sftp.get(remote_file, local_file)
        sftp.close()
        self.ssh.close()

    def put(self, host, username, local_file, remote_file):
        self.ssh.connect(host, username="root", password=None)
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