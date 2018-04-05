# -*- mode: ruby -*-
# # vi: set ft=ruby :

# Vagrant version and Vagrant API version requirements
Vagrant.require_version ">= 1.6.0"
VAGRANTFILE_API_VERSION = "2"

# YAML module for reading box configurations.
require 'yaml'

# Read machine configs from YAML file
machines = YAML.load_file(File.join(File.dirname(__FILE__), 'machines.yml'))

# Create boxes
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Disable updates to keep environment sane.
  config.vm.box_check_update = false

  # Iterate through entries in YAML file
  machines.each do |machine|
    config.vm.define machine["name"] do |box|
      box.vm.box = machine["box"]
      box.vm.hostname = machine["name"]
      box.vm.network "private_network", ip: machine["ip"]

      if machine["script"] != nil
        box.vm.provision :shell, :path => machine["script"]
      end

      if machine["ansible"] != nil
        box.vm.provision "ansible" do |ansible|
            ansible.playbook = machine["ansible"] 
        end
      end

      box.vm.provider :virtualbox do |vb|
        vb.name = machine["name"]
        vb.memory = machine["ram"]

        if machine["gui"] != nil
        	vb.gui = false
        end # end of gui

      end # end of vb provider
    end # end of box
  end # end of machines loop

  config.vm.provision "shell", inline: <<-SHELL
    apt-get install -y avahi-daemon libnss-mdns
  SHELL

end # end of config
