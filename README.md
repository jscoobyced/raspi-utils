## Raspberry Pi utilities

Various utilities for Raspberry Pi extensions and modules.

# Cooling fan

To install the scripts at boot for the [cooling fan](https://www.cytron.io/c-raspberry-pi/c-raspberry-pi-hat/c-hat-for-rpi-4/p-rgb-cooling-hat-with-fan-and-oled-for-4b-3b-plus-3b):
```
cd /tmp
git clone https://github.com/jscoobyced/raspi-utils
cd /tmp/raspi-utils
sudo mv cooling-hat-oled /opt/cooling-fan
cd /opt/cooling-fan
sudo ./install.sh
```