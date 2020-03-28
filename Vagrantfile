
Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/vagrant_data"

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 4
  end

  #Ejecucion de shell de inicio 
  config.vm.provision "shell", inline: <<-SHELL

    # instalar firefox
    sudo apt update
    sudo apt -y install firefox

    # instalar chromium
    sudo apt-get install -y chromium-browser

    # instalar y actualizar python/pip 3
    sudo apt install -y python3
    sudo apt install -y python3-pip
    pip3 install --upgrade --ignore-installed urllib3

    # descarga el geckodriver (driver para firefox)
    sudo apt-get -y install wget
    sudo mkdir /usr/bin/webdrivers
    cd /usr/bin/webdrivers
    wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
    sudo tar -xf geckodriver-v0.26.0-linux64.tar.gz

    # instala firefox version 64
    cd ~
    wget https://ftp.mozilla.org/pub/firefox/releases/64.0/linux-x86_64/en-US/firefox-64.0.tar.bz2
    tar -xjf firefox-64.0.tar.bz2
    sudo su
    sudo mv firefox /opt/

    # descarga el driver de chrome
    sudo apt-get install -y unzip
    sudo mkdir /usr/bin/webdrivers
    wget https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip
    sudo unzip chromedriver_linux64.zip
    sudo rm -fr chromedriver_linux64.zip
    sudo ln -s /opt/firefox/firefox /usr/bin/firefox

    # instala selenium 
    sudo pip3 install selenium

  SHELL
end
