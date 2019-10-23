# Ansible Role: Gauntlt 

Installs Gauntlt, a ruggedization framework that helps in security testing by devs, ops and security.

## Requirements
This role needs ruby installed globally via rvm_io.ruby role.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    gauntlt_version: "0.10.8"

## Dependencies

None.

## Example Playbook

	  - hosts: servers
	    vars:
	      # ruby installation via rvm
	      ruby_version: 'ruby-2.6.5'
	      rvm1_rubies: ['{{ ruby_version }}']
	      rvm1_user: 'root'
	      rvm1_install_path: '/usr/local/rvm'
	
	    roles:
	      - rvm_io.ruby
	      - secfigo.gauntlt

## License

MIT

## Author Information

This role was created in 2017 by [Mohammed A. Imran](https://www.secfigo.com/), author of [Practical DevSecOps Course](https://www.teachera.io/devsecops-course/).
