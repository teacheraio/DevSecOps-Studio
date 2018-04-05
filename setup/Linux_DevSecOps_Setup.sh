#!/bin/bash

echo "This script will setup the initial environment required for DevSecOps Studio";

#variables
ansible_repo="deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main"
virtualbox_repo="deb https://download.virtualbox.org/virtualbox/debian stretch contrib"
devsecops_studio_git="https://github.com/teacheraio/DevSecOps-Studio.git"

#functions
function cache_update {
    apt-get update 
}

function repos_add {

    grep -hq "$ansible_repo" /etc/apt/sources.list;
    if [ $? -ne 0 ]; then
	echo "Adding Ansible Repo";
	echo "$ansible_repo" >> /etc/apt/sources.list ;
	apt-get update; apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367;
    else
	echo "Ansible repo exists";
    fi
    
    grep -hq "$virtualbox_repo" /etc/apt/sources.list;
    if [$? -ne 0 ]; then
	echo "Adding Virtualbox Repo";
	echo "$virtualbox_repo" >> /etc/apt/sources.list;
	apt-get update ;
	wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add -;
	wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add -;
    else
	echo " Virtualbox repo exists";
    fi
}

function apps_install {
   apt-get install git ansible vagrant virtualbox-5.2 -y ;
}

function devsecops-studio_setup {
    echo "Setting up DevSecOps Studio";
    su -l $USERNAME -c "git clone $devsecops_studio_git ~/DevSecOps-Studio && ansible-galaxy install -r ~/DevSecOps-Studio/requirements.yml -p ~/DevSecOps-Studio/provisioning/roles &&  cd ~/DevSecOps-Studio/ && vagrant up";
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

#execution

#updating system cache
#cache_update

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

#settingup of DevSecOps Studio
dpkg -l git vagrant virtualbox ansible
if [ $? -ne 0 ];then
    echo "Make sure Virtualbox, Vagrant, Ansilble & Git are installed"
else
    devsecops-studio_setup
fi


