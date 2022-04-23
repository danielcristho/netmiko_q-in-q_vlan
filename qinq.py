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

def conf_int(conn,conf_int):
    vlanInterface1 = conf_int['interface1']
    interface = conf_int['interface']
    list_conf = ['interface vlan add name=vlan10 use-service-tag=yes', 
                '{}'.format(vlanInterface1), '{}'.format(interface)]

    print (conn.send_config_set(list_conf))

def conf_ip(conn, ip_config):
    interface = ip_config['interface']
    ip_addr = ip_config['ip_address']
    list_conf = ['ip address add interface= {}'.format(interface),
                '{}'.format(ip_addr)]

    print (conn.send_config_set(list_conf))            