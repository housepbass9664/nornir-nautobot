from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko.tasks import netmiko_send_config


nr = InitNornir(config_file='config.yml')

def send_configs(task):
    task.host.defaults.username = 'admin'
    task.host.defaults.password = 'admin'
    task.run(task=netmiko_send_config, config_file=f"{task.host.platform}/ad_hoc_cmds.txt")

output = nr.run(task=send_configs)
print_result(output)