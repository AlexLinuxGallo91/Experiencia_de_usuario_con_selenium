# Experiencia de usuario con selenium
Experiencia y testing de experiencia de usuario (OWA) con python

## Dependencias 
* Ubuntu Server
* Oracle Virtual Box (donde se generaran nuestros ambientes/vm de prueba para ejecutar nuestro script)
* Vagrant
* Python/PIP (version 3)
* GeckoDriver (driver para el manejo del navegador firefox con selenium)

### Oracle Virtual Box
Es necesario instalarlo en nuesto SO, esto con el fin de que se creen nuestros ambientes/vm de prueba mediante Vagrant, [Dale clic aqui para instalarlo](https://www.virtualbox.org/wiki/Downloads "Oracle Virtual Box's Download page")

### Vagrant
Se utilizo Vagrant, con el fin de generar un ambiente prueba con Ubuntu Server, se comparte el link para su instalacion (no es necesaria su instalacion, solo es para crear un ambiente de prueba):

[Instalar Vagrant](https://www.vagrantup.com/downloads.html "Vagrant's Download page")

Despues de instalarlo en nueso SO, tendremos que navegar en cualquier terminal dentro de la carpeta del proyecto y ejecutar el siguiente comando

```
vagrant up
```

Lo que hara este comando, es crear nuestra maquina virtual por medio de un script el cual esta contenido dentro del archivo **Vagrantfile**, el cual tambien descargara la imagen/box del linux Ubuntu Server.

Una vez que inicie el ambiente, se ejecutara un Shell Script el cual instalara las dependencias necesarias para poder ejecutar el script de experiencia de usuario, estas dependencias estan descritas dentro del archivo **Vagrantfile**

```
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

```
Una vez finalizado la instalacion de dependencias, se podra acceder al ambiente desde la terminal con el comando 
```
vagrant ssh
```
o se puede conectar desde algun cliente SSH como puttyh con los siguientes datos
```
ip: 127.0.0.1
user: vagrant
password: vagrant
```

y podremos ejecutar con exito el script de experiencia de usuario desde la terminal (dentro de la carpeta del proyecto) con el siguiente comando:

```
python3 inicio.py
```

