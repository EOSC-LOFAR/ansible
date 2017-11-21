"""
Create a file ~/.surfsara with content:

user=<username>
pass=<password>

"""
import oca
import os
import sys

config_path = os.path.expanduser("~/.surfsara")
endpoint = 'https://api.hpccloud.surfsara.nl/RPC2'

def main():
    if not os.access(config_path, os.R_OK):
        print("can't read {}".format(config))
        print(__doc__)
        sys.exit(1)


    config = {}
    with open(config_path, 'r') as f:
        for l in f:
            s = l.strip().split('=')
            if len(s) == 2:
                config[s[0]] = s[1]

    if not ('user' in config and 'pass' in config):
        print("can't find user and/or pass in config")
        print(__doc__)
        sys.exit(1)

    client = oca.Client(config['user'] + ':' + config['pass'], endpoint)
    vp = oca.VirtualMachinePool(client)
    vp.info()
    print("[nodes]")
    for vm in vp:
        ip_list = list(v.ip for v in vm.template.nics)
        #print("{} {} {} (memory: {} MB)".format(vm.name, ip_list, vm.str_state, vm.template.memory))
        print(ip_list[0])

if __name__ == '__main__':
    main()
