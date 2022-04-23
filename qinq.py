import yaml
from pprint import pprint
from netmiko import ConnectHandler

def read_inventory(yaml_file):
    with open(yaml_file) as f:
        inventory = f.read()

    inventory_dict = yaml.load(inventory)
    return inventory_dict

def device_connection(router_ip):
    device = {
        "device_type" : "mikrotik_routeros",
        "ip" : router_ip,
        "username" : "admin",
        "password" : "admin123"
    }

    conn = ConnectHandler(**device)
    return conn