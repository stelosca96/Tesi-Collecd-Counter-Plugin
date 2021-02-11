import collectd
import json, time

PATH = '/proc/udp_tcp_counter'


def config_func(config):
    path_set = False
    servers = []

    for node in config.children:
        key = node.key.lower()
        val = node.values[0]

        if key == 'path':
            global PATH
            PATH = val
            path_set = True
        elif key == 'server':
            servers.append(val)
            # todo: penso ci sia qualche problema con la formattazione del testo
        else:
            collectd.info('packet_counter plugin: Unknown config key "%s"' % key)
    

    if path_set:
        collectd.info('packet_counter plugin: Using overridden path %s' % PATH)
    else:
        collectd.info('packet_counter plugin: Using default path %s' % PATH)
    
    servers = [
    "130.192.181.193 80",
    "130.192.181.193 443",
    "216.58.198.3 443",
    "216.58.198.3 80",
    "192.168.1.55 80",
    "192.168.1.55 8096"
]

    collectd.info('packet_counter plugin servers: "%s"' % servers)
    with open(PATH, 'w') as f:
        for server in servers:
            f.write(server + '\n')
            # todo: non so se sia utile, ma ogni tanto evita crash
            time.sleep(0.1)





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
