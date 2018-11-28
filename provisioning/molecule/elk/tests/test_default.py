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
  '/etc/docker/certs.d/gitlab.local:4567',
])
def test_directory_is_present(host, directory):
    dir = host.file(directory)
    assert dir.is_directory
    assert dir.exists


@pytest.mark.parametrize('file', [
  '/etc/hosts',
  '/home/vagrant/.ssh/id_rsa',
  # nginx
  '/etc/nginx/nginx.conf',
  # elastic search
  '/etc/elasticsearch/elasticsearch.yml',
  # kibana
  '/opt/kibana/config/kibana.yml',
  # logstash
  '/etc/init.d/logstash',
])
def test_binary_is_present(host, file):
    file = host.file(file)
    assert file.exists


@pytest.mark.parametrize('pkg', [
  'curl',
  'tree',
  'sshpass',
  'nginx',
])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


@pytest.mark.parametrize('svc', [
  'nginx',
  'elasticsearch',
  'kibana',
  'logstash',
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
  ("nginx -t", "^1.0.0*"),
])
def test_commands(host, command, regex):
    cmd = host.check_output(command)
    assert re.match(regex, cmd)
