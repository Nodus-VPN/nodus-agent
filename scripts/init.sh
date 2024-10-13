#!/bin/bash

apt update -y && apt upgrade -y
apt install openvpn wireguard pip - y

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 20

npm install pm2 -g
pip install -r requirements.txt

pm2 start main.py --interpreter=python3 -- wg_agent
pm2 start main.py --interpreter=python3 -- ovpn_agent
pm2 start main.py --interpreter=python3 -- uptime_agent
pm2 start main.py --interpreter=python3 -- subscription_agent
