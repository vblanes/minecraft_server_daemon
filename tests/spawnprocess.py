from subprocess import Popen, PIPE

Popen('thunderbird', stdin=PIPE, stdout=PIPE)