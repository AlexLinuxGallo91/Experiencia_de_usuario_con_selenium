
Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/vagrant_data"

  #Ejecucion de shell de inicio 
  config.vm.provision "shell", inline: <<-SHELL

    #instalar firefox
    sudo apt update
    sudo apt -y install firefox

    #instalar y actualizar python/pip 3
    sudo apt install -y python3
    sudo apt install -y python3-pip
    pip3 install --upgrade --ignore-installed urllib3

    #descarga el geckodriver (driver para firefox)
    sudo apt-get -y install wget
    sudo mkdir /usr/bin/webdrivers
    cd /usr/bin/webdrivers
    wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
    sudo tar -xf geckodriver-v0.26.0-linux64.tar.gz

    #instala selenium 
    sudo pip3 install selenium

  SHELL
end
