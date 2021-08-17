from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.tasks.data import load_yaml
import requests 
import pynautobot
#disable ssl warnings
requests.packages.urllib3.disable_warnings() 

nb_url = 'https://192.168.254.80'
nb_token = '186a3a79c274bf1c7d5fb0358923c77d4a103e99'
#initialize nautobot api client
nb = pynautobot.api(url=nb_url, token=nb_token)
nb.http_session.verify = False
#initialize nornir
nr = InitNornir(config_file='config.yml')

def apply_vars(task):
    ''' pull context, interface data from nautobot, add to host dict, push through templates'''
    task.host.defaults.username = 'admin'
    task.host.defaults.password = 'admin'
    intf_list = []
    interfaces = nb.dcim.interfaces.filter(device=f'{task.host}')
    ip_addresses = nb.ipam.ip_addresses.filter(device=f'{task.host}')
    for intf in interfaces:
        #simple filter to only select interfaces with attached cables
        if intf.cable_peer:
            intf_dict = {}
            intf_dict['name'] = intf.name
            intf_dict['description'] = intf.description
            intf_dict['mtu'] = intf.mtu
            intf_dict['mode'] = intf.mode
            intf_dict['tagged_vlans'] = intf.tagged_vlans
            intf_dict['untagged_vlan'] = intf.untagged_vlan
            #pull interface ip from ip_addresses endpoint
            for ip_addr in ip_addresses:
                if intf_dict['name'] == ip_addr['assigned_object']['name']:
                    intf_dict['ip_address'] =  ip_addr
            intf_list.append(intf_dict)
    task.host['interfaces'] = intf_list
    #push data through templates
    glob_vars = task.run(task=template_file, template='global_cfg.j2', path=f'{task.host.platform}/templates')
    host_vars = task.run(task=template_file, template='interfaces.j2', path=f'{task.host.platform}/templates')
    config = glob_vars.result + host_vars.result
    #apply configs to host
    task.run(task=napalm_configure, configuration=config, dry_run=True, replace=True)

output = nr.run(task=apply_vars)
print_result(output)