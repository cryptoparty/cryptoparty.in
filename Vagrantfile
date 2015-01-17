# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
  # Box
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = 'cryptoparty'

  # Shared folders
  config.vm.synced_folder '.', '/vagrant'

  # Ports
  config.vm.network :forwarded_port, guest: 5000, host: 5001

  # Setup
  config.vm.provision :shell, :inline => 'echo installing dependencies...'
  config.vm.provision :shell, :inline => 'apt-get update'
  config.vm.provision :shell, :inline => 'apt-get install -y python3 python3-dev build-essential python3-setuptools python3-pip'
  config.vm.provision :shell, :inline => 'apt-get install -y postgresql libpq-dev postgresql-9.3-postgis-2.1 python3-lxml'
  config.vm.provision :shell, :inline => 'sudo pip3 install -r /vagrant/requirements.txt'
  config.vm.provision :shell, :inline => 'echo setting up database'
  config.vm.provision :shell, :inline => 'sudo -u postgres /vagrant/scripts/create_testuser_and_database.sh'

  # VirtualBox
  config.vm.provider :virtualbox do |vb|
    vb.customize ['modifyvm', :id, '--name', 'cryptoparty.vm.raring64']
  end

end
