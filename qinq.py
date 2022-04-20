from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from datetime import datetime
import yaml
import time

if __name__ == '__main__':
    with open('inventory.yaml') as f:
        inventory = yaml.safe_load(f.read())

    credentials = inventory['vars']
    devices = len(inventory['hosts'])
    

#Initialize attributes for establishing connection to target device.
def send_command(dev: dict, cmd: str) -> str:
    hostname = device['hostname']
    del dev['hostname']

    try:
        with ConnectHandler(**dev) as conn:
            conn.enable()
            output = conn.send_command(cmd)
        output = output.strip()
    except NetMikoTimeoutException:
        print("Connection time out")
    except NetMikoAuthenticationException:
        print("Authentication  failed")

    dev['hostname'] = hostname

    return output                