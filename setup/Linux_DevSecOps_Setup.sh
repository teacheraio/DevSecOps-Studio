#!/bin/bash

echo "This script will setup the initial environment required for ascdso-studio";

#variables
ansible_repo="deb http://ppa.launchpad.net/ansible/ansible/ubuntu bionic main"
virtualbox_repo="deb https://download.virtualbox.org/virtualbox/debian stretch contrib"
ascdso_studio_git="https://github.com/Consult2016/ascdso-studio.git"

#functions
function cache_update {
    apt update
}

function repos_add {

    grep -hq "$ansible_repo" /etc/apt/sources.list;
    if [ $? -ne 0 ]; then
	echo "Adding Ansible Repo";
	echo "$ansible_repo" >> /etc/apt/sources.list ;
	apt update; apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367;
    else
	echo "Ansible repo exists";
    fi

    grep -hq "$virtualbox_repo" /etc/apt/sources.list;
    if [$? -ne 0 ]; then
	echo "Adding Virtualbox Repo";
	echo "$virtualbox_repo" >> /etc/apt/sources.list;
	apt update ;
	wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add -;
	wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add -;
    else
	echo " Virtualbox repo exists";
    fi
}

function apps_install {
   apt install git ansible vagrant virtualbox-6.1 -y ;
}

function ascdso-studio_setup {
    echo "Setting up ascdso-studio";
    su -l $USERNAME -c "git clone https://github.com/Consult2016/ascdso-studio.git ~/ascdso-studio && ansible-galaxy install -r ~/ascdso-studio/requirements.yml -p ~/ascdso-studio/provisioning/roles &&  cd ~/ascdso-studio/ && vagrant up";
}

function virtualbox_hostonly_setup {

dpkg -l virtualbox
if [ $? -ne 0]; then
    VBoxManage list hostonlyifs | grep -hq '10.0.1.1'
    if [ $? -ne 0]; then
	VBoxManage hostonlyif create;
	VBoxManage hostonlyif ipconfig $(VBoxManage list hostonlyifs | grep -e "^Name"|cut -d ":" -f2 | sort -ru | head -n1) -ipconfig 10.0.1.1 -netmask 255.255.255.0;
    else
	echo "Hostonly Network of 10.0.1.1 exists";
    fi
else
    echo "Virtualbox need to be installed"
fi
}

# execution

#updating system cache
cache_update

#checking OS & user privileges
if [ "$(uname -o)" == 'GNU/Linux' ]; then
    if [ "$(id -u)" != 0 ]; then
       echo "The following script must run with root privileges"
       exit -1
    else
	repos_add
	apps_install
	virtualbox_hostonly_setup
    fi
else
    echo "The following script works only on Debian based GNU/Linux systems"
    exit -1
fi

#settingup of ascdso-studio
dpkg -l git vagrant virtualbox ansible
if [ $? -ne 0 ];then
    echo "Make sure Virtualbox, Vagrant, Ansilble & Git are installed"
else
    ascdso-studio_setup
fi
