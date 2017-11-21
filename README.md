# ansible
scripts for automated deployment of surfsara HPCcloud nodes

Usage:
* Create a file ~/.surfsara containing:
```
user=<cloud username>
pass=<hpccloud password>
```

now if you run list.py it will return a list of IPs of active VMs.

* Install ansible to configure all these IPs automatically by running:
```
$ make
```
Note that this is just an example to illustrate how this might work.

To make this work you need:
* To have access to HPC cloud
* Have some VM's deployed
* Have a pub/priv keypair configured (before you created the VMs)
* For now Ubuntu 16.04 is assumed as target VM.


The script will:
* Enable KERN-3
* Install the latest docker
* Install toil and the CWL rererence runner.
