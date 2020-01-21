
Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/vagrant_data"

  #Ejecucion de shell de inicio 
  config.vm.provision "shell", inline: <<-SHELL

    # instalar firefox
    sudo apt update
    sudo apt -y install firefox

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

    # instala selenium 
    sudo pip3 install selenium

    # instala el conector de mysql para python 
    sudo pip3 install mysql-connector-python

    # instala MYSQL 
    debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
    debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
    apt-get update
    apt-get install -y mysql-server

    # ejecuta el script de python (ETL) para la creacion de la base, tabla e insercion de datos
    cd /vagrant_data
    python3 insercion_datos_mysql.py

  SHELL
end
