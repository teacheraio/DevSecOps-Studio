import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

# TODO implement running as user, gauntlt checks and jenkins url, \
#       jenkins plugins and username and password


@pytest.mark.parametrize('pkg', [
  'curl',
  'sshpass',
  'docker-ce',
  'nikto',
  'nmap',
  'sqlmap',
  'jenkins'
])
def test_pkg(host, pkg):
    package = host.package(pkg)
    assert package.is_installed


@pytest.mark.parametrize('directory', [
  '/etc/docker/certs.d/gitlab.local:4567',
  '/var/lib/jenkins'
])
def test_directory_is_present(host, directory):
    dir = host.file(directory)
    assert dir.is_directory
    assert dir.exists


@pytest.mark.parametrize('file', [
  '/etc/hosts',
  '/usr/bin/docker',
  '/usr/bin/java',
  '/opt/jenkins-cli.jar',
  '/usr/local/bin/packer',
  '/usr/local/bin/terraform',
  '/usr/local/bin/ansible',
  '/usr/local/bin/ansible-lint',
  '/usr/local/bin/docker-compose',
  '/etc/docker/certs.d/gitlab.local:4567/ca.crt'
])
def test_binary_is_present(host, file):
    file = host.file(file)
    assert file.exists


@pytest.mark.parametrize('command, regex', [
  ("sslyze --version", "^1.4.3*"),
])
def test_commands(host, command, regex):
    cmd = host.check_output(command)
    assert re.match(regex, cmd)


@pytest.mark.parametrize('svc', [
  'docker',
  'jenkins'
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
