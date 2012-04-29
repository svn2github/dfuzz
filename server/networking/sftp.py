import os
import paramiko
#yum install python-paramiko

ssh = paramiko.SSHClient()
password = raw_input("enter your password")
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect("192.168.1.90", username="root", password=password)
sftp = ssh.open_sftp()
source = "test.txt"
destination = "/root/test.txt"
sftp.put(source, destination)
sftp.close()
ssh.close()