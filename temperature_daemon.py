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
    # https://stackoverflow.com/questions/26688936/how-to-get-pid-by-process-name
    return map(int, check_output(["pidof",name]).split())

def temperature_check(min_temp, max_temp, run_server_command, temp_path):
    # get temperature
    temperature = get_temperature(temp_path)
    # check if minecraft is running
    pids = get_pid('java')
    # if temperature is above threshold try to kill minecraft
    if temperature >= max_temp and pids:
        for pid in pids:
            kill(pid, signal.SIGSTOP)
    # if temperature is below other treshold
    # run minecraft server if nots running
    elif temperature <= min_temp and not pids:
        Popen(run_server_command, stdin=PIPE, stdout=PIPE)

def Main(min_temp, max_temp, run_com, temp_path):
    with daemon.DaemonContext():
        # call cmain functionality
        temperature_check(min_temp=min_temp,max_temp=max_temp, 
                            run_server_command=run_com, temp_path=temp_path)
        # wait time to check again
        # can be improved by chaching time using return values
        time.sleep(30)

if __name__ == '__main__':
    # use argparse to make it handsome and avoid environ vars
    parser = argparse.ArgumentParser(description="Daemon for temperature safety\
        running minecraft server on raspberry pi 4 / ubuntu arm")
    
    parser.add_argument('--minimum-temperature', '-min',
        help='Minimum temperature. Run the server if actual temps is lower than this')
    
    parser.add_argument('--maximum-temperature', '-max', 
        help='Maximum temperature. Close the server at this this temperature')
    
    parser.add_argument('--run-server-command', '-run',
        default='java -Xmx768M -Xms512M -jar /opt/minecraft/minecraft_server.1.15.2.jar nogui',
        help='Command to run the server. Beware of the paths!')

    parser.add_argument('--temperature-file-path', '-temp',
        default='/sys/class/thermal/thermal_zone0/temp',
        help='Path to the file where the current temp is')
    

    args = parser.parse_args()
    min_ = float(args.min)
    max_ = float(args.max)
    run_com_ = args.run
    temp_path_ = args.temp
    Main(min_, max_, run_com_, temp_path_)

    

