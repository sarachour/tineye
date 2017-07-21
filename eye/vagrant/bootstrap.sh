#!/bin/bash

echo "==== BOOSTRAP ROOT ==="
export DEBIAN_FRONTEND=noninteractive
apt-get update

echo "Installing DebConf"
apt-get install debconf-utils -y > /dev/null

echo "Install Dynamorio requirements"
sudo apt-get install cmake g++ g++-multilib doxygen transfig imagemagick ghostscript git
apt-get install m4 git -y > /dev/null


echo "Install Go"
sudo apt-get install -y build-essential golang

echo "Install Python"
apt-get install python python-pip -y > /dev/null
pip install --upgrade pip

echo "Install Python Dependencies"
pip install scipy numpy sympy  > /dev/null


