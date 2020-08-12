import daemon
import time
from subprocess import check_output, Popen, PIPE
from os import kill
import signal
import argparse

def get_temperature(temp_file_path):
    try:
        with open(temp_file_path, 'r') as temp_file:
            return float(temp_file.read().strip())/1000
    except IOError:
        return -1

def get_pid(name):
    try:
        return [int(p) for p in check_output(["pidof",name]).split()]
    # throws an exception is there no process with that name
    except:
        return []

def temperature_check(min_temp, max_temp, temp_path):
    # get temperature
    temperature = get_temperature(temp_path)
    # check if minecraft is running
    pids = get_pid('java')
    # if temperature is above threshold try to kill minecraft
    if temperature >= max_temp and pids:
        for pid in pids:
            kill(pid, signal.SIGKILL)
    # if temperature is below other treshold
    # run minecraft server if nots running
    elif temperature <= min_temp and not pids:
        # IMPORTANT: this is my personal conf!!
        # edit this command to your conf or the use of other program!!
        Popen(['java', '-Xmx2048M','-jar', 'minecraft_server.1.15.2.jar', 'nogui'], 
            stdin=PIPE, stdout=PIPE, cwd='/opt/minecraft/')

def Main(min_temp, max_temp, temp_path, sleep_time):
    with daemon.DaemonContext():
        # call cmain functionality
        temperature_check(min_temp=min_temp,max_temp=max_temp, temp_path=temp_path)
        # wait time to check again
        # can be improved by chaching time using return values
        time.sleep(sleep_time)

if __name__ == '__main__':
    # use argparse to make it handsome and avoid environ vars
    parser = argparse.ArgumentParser(description="Daemon for temperature safety\
        running minecraft server on raspberry pi 4 / ubuntu arm")
    
    parser.add_argument('--min', '-minimum-temperature',
        help='Minimum temperature. Run the server if actual temps is lower than this')
    
    parser.add_argument('--max', '-maximum-temperature', 
        help='Maximum temperature. Close the server at this this temperature')

    parser.add_argument('--sleep', '-sleep-time-daemon', default=10,
        help='How many seconds the daemon should sleep between checks')

    parser.add_argument('--temp', '-temperature-file-path',
        default='/sys/class/thermal/thermal_zone0/temp',
        help='Path to the file where the current temp is')
    

    args = parser.parse_args()
    min_ = float(args.min)
    max_ = float(args.max)
    sleep_time = int(args.sleep)
    temp_path_ = args.temp
    Main(min_, max_, temp_path_, sleep_time)

    

