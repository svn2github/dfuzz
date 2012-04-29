import os
import paramiko
#yum install python-paramiko
#http://www.lag.net/paramiko/docs/


#ssh-keygen
#ssh-copy-id 192.168.1.90


host = "192.168.1.90"
ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(host, username="root", password=None)
sftp = ssh.open_sftp()
local_file = "test.txt"
remote_file = "/root/test.txt"
#sftp.put(local_file, remote_file)
sftp.get(remote_file, local_file)
sftp.close()
ssh.close()