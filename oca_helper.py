"""
Create a file ~/.surfsara with content:

user=<username>
pass=<password>

Also you need to do some tasks manually since the OCA API is an unmaintained
"enfant terrible":

 * login to https://ui.hpccloud.surfsara.nl/
 * make sure you are in the user view
 * go to Apps
 * select an "app" (like Ubuntu-16.04.3-Server (2017-12-07)) and press
   "openNebula"
 * select local_images_ssh datastore and then press "download"
 * Go to VM Templates view and notice VM template ID. Use that ID
   on the CLI or change in this script.

"""
import click
import oca
import os
import sys

# settings
DEFAULT_TEMPLATE_ID = 7890
DEFAULT_MEMORY = 2048  # GB
DEFAULT_CPU = 4
DEFAULT_VCPU = 4
DEFAULT_NODES_NUM = 10

# you probably don't want to change these
config_path = os.path.expanduser("~/.surfsara")
endpoint = 'https://api.hpccloud.surfsara.nl/RPC2'


def read_config():
    if not os.access(config_path, os.R_OK):
        print("can't read {}".format(config_path))
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
    return config


def init_client(config, endpoint):
    return oca.Client(config['user'] + ':' + config['pass'], endpoint)


@click.group()
@click.pass_context
def cli(context):
    config = read_config()
    context.obj = init_client(config, endpoint)


@cli.command()
@click.pass_obj
def iplist(client):
    vp = oca.VirtualMachinePool(client)
    vp.info()
    click.echo("[nodes]")
    for vm in vp:
        ip_list = list(v.ip for v in vm.template.nics)
        click.echo(ip_list[0])


@cli.command()
@click.option('--memory', default=DEFAULT_MEMORY)
@click.option('--cpu', default=DEFAULT_CPU)
@click.option('--vcpu', default=DEFAULT_VCPU)
@click.option('--number', help='Number of nodes', default=DEFAULT_NODES_NUM)
@click.option('--template_id', default=DEFAULT_TEMPLATE_ID)
@click.pass_obj
def create(client, memory, cpu, vcpu, number, template_id):
    extra_template = """
    MEMORY = {}
    CPU = {}
    VCPU = {}
    """.format(memory, cpu, vcpu)
    tp = oca.VmTemplatePool(client)
    tp.info()
    template = tp.get_by_id(template_id)
    for i in range(number):
        name = "workflow-{}".format(i)
        click.echo("creating node '{}'".format(name))
        template.instantiate(name=name, extra_template=extra_template)


@cli.command()
@click.pass_obj
def destroy(client):
    vmp = oca.VirtualMachinePool(client=client)
    vmp.info()
    for i in vmp:
        click.echo("destroying node '{}'".format(i.name))
        i.delete()


if __name__ == '__main__':
    cli()
