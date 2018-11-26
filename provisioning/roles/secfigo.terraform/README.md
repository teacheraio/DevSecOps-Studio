# Ansible Role: Terraform

[![Build Status](https://travis-ci.org/secfigo/ansible-role-terraform.svg?branch=master)](https://travis-ci.org/secfigo/ansible-role-terraform)

Installs Hashicorp's [Terraform](https://www.terraform.io), a tool for building, changing, and combining infrastructure safely and efficiently.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    terraform_version: "0.11.10"

The Packer version to install.

    terraform_arch: "amd64"

The system architecture (e.g. `386` or `amd64`) to use.

    terraform_bin_path: /usr/local/bin

The location where the Packer binary will be installed (should be in system `$PATH`).

## Dependencies

None.

## Example Playbook

    - hosts: servers
      roles:
        - secfigo.terraform

## License

MIT

## Author Information

This role was created in 2017 by [Mohammed A. Imran](https://www.secfigo.com/), author of [Practical DevSecOps Course](https://www.teachera.io/devsecops-course/).
