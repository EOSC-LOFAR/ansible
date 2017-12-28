
all: ansible

.virtualenv/:
	python -p python2 .virtualenv/
	.virtualenv/bin/pip install -r requirements.txt

hosts: .virtualenv/
	.virtualenv/bin/python oca_helper.py iplist > hosts

ansible: hosts
	ansible-playbook -i hosts site.yml

create: .virtualenv/
	.virtualenv/bin/python oca_helper.py create

destroy: .virtualenv/
	.virtualenv/bin/python oca_helper.py destroy

