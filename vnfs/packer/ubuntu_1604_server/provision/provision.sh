#!/bin/bash

useradd -m -s /bin/bash -p $(openssl passwd -crypt $guest_user) -U $guest_password
echo "$guest_user ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers

# Bypass proxy settings if http_proxy is empty
if [ ! -z "$http_proxy" ]
then
    echo "http_proxy=$http_proxy" | sudo tee -a /etc/environment
    echo "https_proxy=$https_proxy" | sudo tee -a /etc/environment
    echo "HTTP_PROXY=$http_proxy" | sudo tee -a /etc/environment
    echo "HTTPS_PROXY=$https_proxy" | sudo tee -a /etc/environment
    if [ ! -f /etc/apt/apt.conf ]; then
        sudo touch /etc/apt/apt.conf
    fi
    echo 'Acquire::http::Proxy "'$http_proxy'";' | sudo tee -a /etc/apt/apt.conf
    echo 'Acquire::https::Proxy "'$https_proxy'";' | sudo tee -a /etc/apt/apt.conf
fi

sudo apt-get -y update
sudo apt-get -y upgrade

# assumes the user-defined startup.sh script has already been copied under /etc/init.d
sudo mv /tmp/startup.sh /etc/init.d/startup.sh
sudo chmod ugo+x /etc/init.d/startup.sh
sudo update-rc.d startup.sh defaults
