# ansible

scripts for automated deployment of surfsara HPCcloud nodes. It will
install all requirements to run the EOSC-LOFAR pipelines in all it forms.

Note that this is just an example to illustrate how this might work and is
not intended for end user usage. The makefile is a collection of example
commands.

# requirements

To make this work you need:
* To have access to HPC cloud
* Have a pub/priv keypair configured before you created any of the VM's
* Prepared a VM template in the UI (see oca_helper.py)
* Have ansible, python virtualenv and make installed on the system where you
  run this script


# usage
* Create a file ~/.surfsara containing:
```
user=<cloud username>
pass=<hpccloud password>
```

now to create some nodes run:
```
make create
```

To destroy all nodes:
```
make destroy
```

To install all software all nodes run:
```
make ansible
```

