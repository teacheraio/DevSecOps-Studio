import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize('directory', [
  '/home/vagrant/.ssh',
  '/home/vagrant/ansible-os-hardening',
  '/home/vagrant/DevSecOps-Studio',
  '/home/vagrant/linux-baseline',
  '/home/vagrant/cis-docker-benchmark',
  '/etc/docker/certs.d/gitlab.local:4567',
])
def test_directory_is_present(host, directory):
    dir = host.file(directory)
    assert dir.is_directory
    assert dir.exists


@pytest.mark.parametrize('file', [
  '/etc/hosts',
  '/home/vagrant/.ssh/id_rsa',
  '/usr/bin/pip',
  '/usr/bin/docker',
  '/usr/local/bin/packer',
  '/usr/local/bin/terraform',
  '/usr/local/bin/ansible',
  '/usr/local/bin/ansible-lint',
  '/usr/local/bin/docker-compose',
  '/usr/local/rvm/rubies/ruby-2.3.1/bin/ruby'
])
def test_binary_is_present(host, file):
    file = host.file(file)
    assert file.exists


@pytest.mark.parametrize('pkg', [
  'curl',
  'tree',
  'sshpass'
])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


@pytest.mark.parametrize('svc', [
  'docker'
])
def test_svc(host, svc):
    service = host.service(svc)

    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('file, content', [
  ("/etc/passwd", "root")
])
def test_files(host, file, content):
    file = host.file(file)

    assert file.exists
    assert file.contains(content)


@pytest.mark.parametrize('command, regex', [
  ("packer --version", "^1.0.0*"),
  ("sudo su -c 'inspec --version' -l vagrant", "^3.0.52*")
])
def test_commands(host, command, regex):
    cmd = host.check_output(command)
    assert re.match(regex, cmd)
