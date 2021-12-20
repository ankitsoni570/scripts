#!/bin/bash -x

echo "------------installing docker"

echo "installing yum-utils"
sudo yum install -y yum-utils

echo "adding repo"
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

sudo  sed -i "s/\$releasever/7/g"  /etc/yum.repos.d/docker-ce.repo

echo "installing docker"
sudo yum install docker-ce

echo "configuring user"
sudo groupadd docker
sudo usermod -aG docker $USER

echo "configuring docker folder"
sudo mkdir /mnt/data/docker
config="{\n\"data-root\": \"/mnt/data/docker\"\n}"
echo -e "$config" | sudo tee /etc/docker/daemon.json > /dev/null

echo "starting docker"
sudo service docker start
