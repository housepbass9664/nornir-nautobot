from nornir import InitNornir
from rich import print as rprint
import requests 
import pynautobot

requests.packages.urllib3.disable_warnings() 

nr = InitNornir(config_file='config.yml')

nb_url = 'https://192.168.254.80'
nb_token = '186a3a79c274bf1c7d5fb0358923c77d4a103e99'

nb = pynautobot.api(url=nb_url, token=nb_token)
nb.http_session.verify = False

def get_data(task):
    print(task.host)
    intf_list = []
    interfaces = nb.dcim.interfaces.filter(device=f'{task.host}')
    ip_addresses = nb.ipam.ip_addresses.filter(device=f'{task.host}')
    for intf in interfaces:
        if intf.cable_peer:
            intf_dict = {}
            intf_dict['name'] = intf.name
            intf_dict['description'] = intf.description
            intf_dict['mtu'] = intf.mtu
            intf_dict['mode'] = intf.mode
            intf_dict['tagged_vlans'] = intf.tagged_vlans
            intf_dict['untagged_vlan'] = intf.untagged_vlan
            for ip_addr in ip_addresses:
                if intf_dict['name'] == ip_addr['assigned_object']['name']:
                    intf_dict['ip_address'] =  ip_addr
            intf_list.append(intf_dict)
    task.host['interfaces'] = intf_list
    rprint(task.host['interfaces'])
    
nr.run(task=get_data)


