import os
import pytest
# import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('pkg', [
  'curl',
  'sshpass',
])
def test_pkg(host, pkg):
    package = host.package(pkg)
    assert package.is_installed


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


# @pytest.mark.parametrize('directory', [
#   '/home/deploy_user/.ssh',
# ])
# def test_directory_is_present(host, directory):
#     dir = host.file(directory)
#     assert dir.is_directory
#     assert dir.exists


@pytest.mark.parametrize('file', [
  '/etc/hosts',
  '/etc/gitlab/gitlab.rb',
  '/etc/gitlab/ssl/gitlab.local.crt',
  '/etc/gitlab/ssl/gitlab.local.key',
])
def test_binary_is_present(host, file):
    file = host.file(file)
    assert file.exists


# @pytest.mark.parametrize('command, regex', [
#   ("getent passwd vagrant", "^vagrant*"),
# ])
# def test_commands(host, command, regex):
#     cmd = host.check_output(command)
#     assert re.match(regex, cmd)


# @pytest.mark.parametrize('svc', [
#   'ssh'
# ])
# def test_svc(host, svc):
#     service = host.service(svc)
#
#     assert service.is_running
#     assert service.is_enabled


@pytest.mark.parametrize('file, content', [
  ("/etc/passwd", "root")
])
def test_files(host, file, content):
    file = host.file(file)

    assert file.exists
    assert file.contains(content)
