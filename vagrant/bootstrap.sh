#!/bin/bash

echo "==== BOOSTRAP ROOT ==="
export DEBIAN_FRONTEND=noninteractive
apt-get update

echo "Installing DebConf"
apt-get install debconf-utils -y > /dev/null

echo "Install Ethereum"
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get install ethereum

#echo "Install Javascript"
#curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
#sudo apt-get install -y nodejs
#sudo npm install npm@latest -g
#curl https://install.meteor.com | sh
echo "Install Python"
apt-get install python python-pip -y > /dev/null
pip install --upgrade pip

echo "Install Python Dependencies"
pip install scipy numpy > /dev/null

echo "Install Web3"
sudo pip install web3




