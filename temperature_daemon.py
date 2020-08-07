import daemon
import time
from subprocess import check_output, Popen, PIPE
from os import kill
import signal

def get_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
            return float(temp_file.read().strip())/1000
    except IOError:
        return -1

def get_pid(name):
    # https://stackoverflow.com/questions/26688936/how-to-get-pid-by-process-name
    return map(int, check_output(["pidof",name]).split())

def temperature_check(low_thresh, high_thresh):
    # TODO parametrize this
    run_server_command = 'java -Xmx768M -Xms512M -jar /opt/minecraft/minecraft_server.1.15.2.jar nogui'
    # get temperature
    temperature = get_temperature()
    # check if minecraft is running
    pids = get_pid('java')
    # if temperature is above threshold try to kill minecraft
    if temperature >= high_thresh and pids:
        for pid in pids:
            os.kill(pid, signal.SIGSTOP)
    # if temperature is below other treshold
    # run minecraft server if nots running
    elif temperature <= low_threshold and not pids:
        Popen(run_server_command, stdin=PIPE, stdout=PIPE)

