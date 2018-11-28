# Testing the boxes and roles locally

## Pre-requisites
You need to have following dependencies installed, we recommend you use `virtualenv` to create virtual environment for python (see travis script for commands)

### Commands to setup
Assuming python and virtualenv is installed

```bash
$ virtualenv env
$ source/env/bin/activate
(env) $ pip install docker molecule==2.19

# We need to create docker container for a particular box, obviously for testing needs
(env) $ molecule create -s devsecops # other options include jenkins, gitlab, gitlab-runner

# Next run the ansible script to provision the container
(env) $ molecule converge -s devsecops

# Finally we test our changes with the scripts under tests/test_default.py
(env) $ molecule verify -s devsecops
```

### Dependencies
- Docker
- Ansible
- Ansible lint
- Python
- Molecule

> You can obviously test using vagrant setup but molecule tests are much faster and follows TDD.

### References
- https://hashbangwallop.com/tdd-ansible.html#abstract
- https://zapier.com/engineering/ansible-molecule/
- https://blog.opsfactory.rocks/testing-ansible-roles-with-molecule-97ceca46736a

### Challenges
- Checking against version output of a command is choppy at best, instead rely on file availability.
