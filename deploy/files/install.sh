#!/bin/bash

echo "Switching to Tue-guest network to update system, you will experience a momentary connection drop!"
sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.old
sudo cp wpa_supplicant.conf.tue_guest /etc/wpa_supplicant/wpa_supplicant.conf
sudo wpa_cli -i wlan0 reconfigure
sudo wpa_cli -i wlan0 reconnect
sleep 1

echo "Logging in to portal"

until $(curl --output /dev/null --silent --head --fail https://google.com); do
    sleep 1
    echo "Connecting via portal"
    DATA=$(curl -s 'https://controller.access.network/portal_api.php' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' --data 'action=subscribe&type=one&connect_policy_accept=false&prefix=&phone=&policy_accept=true')
    LOGIN=$(echo $DATA | grep -oP '\"login\":\"\K\w+')
    PASSWORD=$(echo $DATA | grep -oP '\"password\":\"\K\w+')
    curl -s 'https://controller.access.network/portal_api.php' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' --data "action=authenticate&login=$LOGIN&password=$PASSWORD&policy_accept=false&from_ajax=true"
done

echo "Installing dependencies"
sudo apt-get update
sudo apt-get install -y arduino-mk python3 python3-serial

echo "Reconnecting to internal network"
sudo mv /etc/wpa_supplicant/wpa_supplicant.conf.old /etc/wpa_supplicant/wpa_supplicant.conf
sudo wpa_cli -i wlan0 reconfigure
sudo wpa_cli -i wlan0 reconnect
sleep 1
