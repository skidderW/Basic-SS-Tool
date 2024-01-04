import psutil
import wmi
import subprocess
import os
import struct
import requests
import json
from time import sleep

username = os.getlogin()
directory_path = f'C:\\Users\\{username}\\AppData\\Local\\Temp'
eredmeny = os.path.join(directory_path, 'tokos.txt')
falj_pet = f'C:\\Users\\{username}\\AppData\\Local\\Temp\\tokos.txt'

dps_strings = {'2022/06/30:11:20:36': 'OP AutoClicker','!2019/03/14:20:01:24': 'OP AutoClicker'}
javaw_strings = {'quick accel': 'Sapphire Ghost Client', 'Thank you for choosing Vape V4!': 'Vape V4'}

def get_system_bit():
    bit_size = struct.calcsize("P") * 8
    return bit_size

def find_service_pid(service_name):
    c = wmi.WMI()
    for process in c.Win32_Service():
        if process.Name.lower() == service_name.lower():
            for p in psutil.process_iter(['pid', 'name']):
                if p.info['name'].lower() == 'svchost.exe' and p.pid == process.ProcessId:
                    return p.pid
    return None

def get_process_with_highest_cpu(process_names):
    max_cpu_pid = None
    max_cpu_percent = 0

    for name in process_names:
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] == name:
                pid = proc.info['pid']
                cpu_percent = psutil.Process(pid).cpu_percent(interval=1)
                if cpu_percent > max_cpu_percent:
                    max_cpu_percent = cpu_percent
                    max_cpu_pid = pid

    return max_cpu_pid

def scan_process_strings(process_pid, strings_to_find, strings_file):
    command = f'C:\\Users\\{username}\\AppData\\Local\\Temp\\xxstrings.exe -p {process_pid}'
    process = subprocess.Popen(command, shell=True, cwd=directory_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    output = output.decode("utf-8")
    error = error.decode("utf-8")
    with open(strings_file, "a") as file:
        for line in strings_to_find:
            if line.lower() in output.lower():
                detection = strings_to_find.get(line)
                file.write(detection + "\n")

def main():
    system_bit = get_system_bit()

    process_names = ["javaw.exe", "java.exe"]
    javaw_pid = get_process_with_highest_cpu(process_names)

    service_dps = 'DPS'
    dps_pid = find_service_pid(service_dps)

    if system_bit > 5:
        url = 'https://cdn.discordapp.com/attachments/1005221024180228206/1147489764103172158/xxstrings64.exe'
        strings2_path = f'C:\\Users\\{username}\\AppData\\Local\\Temp\\xxstrings64.exe'
    else:
        url = 'https://cdn.discordapp.com/attachments/1005221024180228206/1147489763562098699/xxstrings.exe'
        strings2_path = f'C:\\Users\\{username}\\AppData\\Local\\Temp\\xxstrings.exe'

    subprocess.run(['curl', '-O', url], cwd=directory_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if dps_pid:
        print("Scanning DPS..")
        scan_process_strings(dps_pid, dps_strings, eredmeny)
    else:
        print("DPS Not found")

    if javaw_pid:
        print("Scanning Javaw..")
        scan_process_strings(javaw_pid, javaw_strings, eredmeny)
    else:
        print("Javaw Not found")

    if os.path.exists(falj_pet):
        subprocess.Popen(["start", falj_pet], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        print("Nothing Found")
        sleep(5)
        sys.exit(0)

if __name__ == "__main__":
    main()
