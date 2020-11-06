#!/bin/bash

if [ $UID != 0 ] ;
then
  echo "You must run as root."
fi

echo "Installing Python 3 dependencies"
apt install -y python3-smbus i2c-tools python3-pip python3-pil python3-rpi.gpio python3-setuptools
pip3 install Adafruit-SSD1306

echo "Installing script at boot by systemd"
ln -s /opt/cooling-fan/cooling.service /etc/systemd/system/
systemctl enable cooling.service
systemctl start cooling.service
