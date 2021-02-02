import collectd
import json
import time

PATH = '/proc/udp_tcp_counter'


def config_func(config):
    path_set = False
    servers = ''

    for node in config.children:
        key = node.key.lower()
        val = node.values[0]

        if key == 'path':
            global PATH
            PATH = val
            path_set = True
        elif key == 'servers':
            servers = servers.replace(';', '\n')
        else:
            collectd.info('packet_counter plugin: Unknown config key "%s"' % key)
    with open(PATH, 'w') as f:
        f.write(servers)

    if path_set:
        collectd.info('packet_counter plugin: Using overridden path %s' % PATH)
    else:
        collectd.info('packet_counter plugin: Using default path %s' % PATH)
    



def read_func():
    # Read value
    with open(PATH, 'r') as f:
        json_txt = f.read()
    values = json.loads(json_txt)

    for key in values:
        # Dispatch value to collectd
        val = collectd.Values()
        val.type = 'derive'
        val.plugin_instance = key
        val.type_instance = 'derive'
        val.values = [values[key]]
        val.plugin = 'packet_counter'
        val.dispatch()


collectd.register_config(config_func)
collectd.register_read(read_func)
