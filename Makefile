
all: ansible

.virtualenv/:
	python -p python2 .virtualenv/
	.virtualenv/bin/pip install -r requirements.txt

hosts:
	.virtualenv/bin/python list.py > hosts

ansible: hosts
	ansible-playbook -i hosts site.yml

