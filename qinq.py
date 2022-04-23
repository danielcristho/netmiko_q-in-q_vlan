import yaml
from pprint import pprint
from netmiko import ConnectHandler

def read_inventory(yaml_file):
    with open(yaml_file) as f:
        inventory = f.read()

    inventory_dict = yaml.safe_load(inventory)
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

def conf_int(conn,int_config):
    vlanInterface = int_config['interface']
    interface = int_config['interface']
    list_conf = ['interface vlan add name=vlan10 use-service-tag=yes', 
                '{}'.format(vlanInterface), '{}'.format(interface)]

    print (conn.send_config_set(list_conf))

def conf_ip(conn, ip_config):
    interface = ip_config['interface']
    ip_addr = ip_config['ip_address']
    list_conf = ['ip address add interface= {}'.format(interface),
                '{}'.format(ip_addr)]

    print (conn.send_config_set(list_conf))

def main():
    yaml_file = 'inventory.yaml'
    inventory_dict = read_inventory(yaml_file)
    pprint(inventory_dict)

    for router in inventory_dict['QINQ']:

        router_ip = router['host']
        print("--------------------------------")
        print("Configuring {}".format(router_ip))
        print("--------------------------------")

        conn = device_connection(router_ip)

        #config ip address
        int_config = router['int_conf']
        for conf in int_config:
            conf_ip(conn, conf)

        #config vlan interface
        vlan_config = router['vlan_conf']
        for config in vlan_config:
            conf_int(conn, config)

main()