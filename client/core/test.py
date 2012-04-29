import subprocess
import sys

cmd = ["watch 'echo hi'"]
process = subprocess.Popen(
    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

while True:
    out = process.stdout.read(1)
    if out == '' and process.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()