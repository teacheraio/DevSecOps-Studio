Adding new functionality
=======================
1. Add roles/functionality in usual places like roles and box.yml files
2. Replicate the same in molecule tests under playbook.yml
3. Write TDD tests to validate the ansible scripts

Jenkins Issues:
===============

1. Setup wizard appear even when jenkins.install.runSetupWizard=false

Fix is to add the following to geerlingguy.jenkins role task

```bash
- name: Fix a defect to disable setup wizard
  jenkins_script:
    script: |
      import static jenkins.model.Jenkins.instance as jenkins
      import jenkins.install.InstallState
      if (!jenkins.installState.isSetupComplete()) {
        InstallState.INITIAL_SETUP_COMPLETED.initializeState()
      }
    user: "{{ admin.userid }}"
    password: "{{ admin.password }}"
```

2. Plugin installation fails so added retries, see https://github.com/geerlingguy/ansible-role-jenkins/issues/169
so added following four lines to plugins.yml task  

```bash
  retries: 2                # https://github.com/geerlingguy/ansible-role-jenkins/issues/169
  delay: 3
  register: result            # <<<
  until: result is succeeded  # <<<
 
```

2. Because of a bug, wizard will show even after successful installation of Jenkins

Fix is to add the following task as disable-wizard.yml and call it from main.yml

see https://github.com/geerlingguy/ansible-role-jenkins/issues/181

```bash
- name: Fix a defect to disable setup wizard
  jenkins_script:
    script: |
      import static jenkins.model.Jenkins.instance as jenkins
      import jenkins.install.InstallState
      if (!jenkins.installState.isSetupComplete()) {
        InstallState.INITIAL_SETUP_COMPLETED.initializeState()
      }
    user: "{{ jenkins_admin_username }}"
    password: "{{ jenkins_admin_password }}"
```

Gitlab
=======

- Verify the gitlab works fine locally in VM because of docker bug on Travis

- For molecule tests you need to use the following configs apart from usual provisioning/gitlab.yml

```bash
  vars:
    gitlab_restart_handler_failed_when: false

  pre_tasks:
    - name: Update apt cache.
      apt: update_cache=yes cache_valid_time=600
      when: ansible_os_family == 'Debian'
      changed_when: false

    - name: Remove the .dockerenv file so GitLab Omnibus doesn't get confused.
      file:
        path: /.dockerenv
        state: absent
```

DevSecOps-Box
=============
- Don't forget to add machine's host name in hosts_entry.yml once you a add new box.
- Ensure host entries are working fine in VM, cant test hosts entries in docker because of its nature see - https://stackoverflow.com/questions/28327458/how-to-add-my-containers-hostname-to-etc-hosts
