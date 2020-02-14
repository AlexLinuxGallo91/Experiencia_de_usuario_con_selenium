
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

# descarga el driver de chrome
sudo apt-get install -y unzip
sudo mkdir /usr/bin/webdrivers
wget https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip
sudo unzip chromedriver_linux64.zip
sudo rm -fr chromedriver_linux64.zip

# instala selenium 
sudo pip3 install selenium

# instala el conector de mysql para python 
sudo pip3 install mysql-connector-python