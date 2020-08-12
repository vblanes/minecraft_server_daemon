"""
Tries to kill process by name
"""
from subprocess import check_output, Popen, PIPE
from os import kill
import signal
import argparse

def get_pid(name):
    return [int(p) for p in check_output(["pidof",name]).split()]

pids = get_pid('electron')
for pid in pids:
    kill(pid, signal.SIGKILL)