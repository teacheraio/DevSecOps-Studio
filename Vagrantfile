# -*- mode: ruby -*-
# # vi: set ft=ruby :

# Vagrant version and Vagrant API version requirements
Vagrant.require_version ">= 2.2.7"
VAGRANTFILE_API_VERSION = "2"

# YAML module for reading box configurations.
require 'yaml'

# Read machine configs from YAML file
machines = YAML.load_file(File.join(File.dirname(__FILE__), 'machines.yml'))

# Create boxes
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Disable updates to keep environment sane.
  config.vm.box_check_update = false

  # Disable shared folder, see https://superuser.com/questions/756758/is-it-possible-to-disable-default-vagrant-synced-folder
  config.vm.synced_folder '.', '/home/vagrant/shared/'

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

        vb.customize ["modifyvm", :id, "--groups", "/"]

      end # end of vb provider
    end # end of box
  end # end of machines loop

  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    sudo apt update
    sudo apt install -y avahi-daemon libnss-mdns
    sudo apt install -y gnuupg2 curl vim git build-essential
    sudo apt autoremove
    #
    # Install rvm
    #
    sudo gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
    sudo apt install -y software-properties-common
    sudo curl -sSL https://get.rvm.io | bash -s stable
    sudo su
    source /etc/profile.d/rvm.sh
    #
    #Install ruby latest
    #
    rvm install ruby --latest
    gem install bundler
  SHELL
end # end of config
