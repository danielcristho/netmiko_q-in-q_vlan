from datetime import datetime
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import yaml
import time
import sys

file_log = open("config_log.txt", "a")
# dev: device info
# cmd: command
def send_command(dev: dict, cmd: str) -> str:

    hostname = device['hostname']
    del dev['hostname']

    try:
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            output = ssh.send_command(cmd)
        output = output.strip()
    except NetMikoTimeoutException:
        output = 'Connection timed out'
    except NetMikoAuthenticationException:
        output = 'Authentication failed'

    dev['hostname']  = hostname

    return output

if __name__ == '__main__':
    command = input('\nEnter command: ')

    with open('inventory.yaml') as f:
        inventory = yaml.safe_load(f.read())

    credentials = inventory['vars']
    devices_counter = len(inventory['hosts'])

    print(f'\executing command: {command}\n')

    execution_start_timer = time.perf_counter()

    #loop to repeat command
    for device in inventory['hosts']:
        device.update(credentials)
        print('*** host: {} - ip: {}'.format(device['hostname'],
            device['host']))
        #send command and store results
        result = send_command(device, command)
        print(f'{result}\n')

    elapsed_time = time.perf_counter() -  execution_start_timer
    print(f"\n\"{command}\" executed in {devices_counter} devices in {elapsed_time:0.2f} seconds.\n")
    file_log.write(
        f"logs:[{device['host']}]\n{command}\n{result}\n"
    )

file_log.close()