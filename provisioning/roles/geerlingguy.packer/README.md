# Ansible Role: Packer

[![Build Status](https://travis-ci.org/geerlingguy/ansible-role-packer.svg?branch=master)](https://travis-ci.org/geerlingguy/ansible-role-packer)

Installs [Packer](https://www.packer.io), a Go-based image and box builder.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    packer_version: "1.0.0"

The Packer version to install.

    packer_arch: "amd64"

The system architecture (e.g. `386` or `amd64`) to use.

    packer_bin_path: /usr/local/bin

The location where the Packer binary will be installed (should be in system `$PATH`).

## Dependencies

None.

## Example Playbook

    - hosts: servers
      roles:
        - geerlingguy.packer

## License

MIT / BSD

## Author Information

This role was created in 2017 by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).
