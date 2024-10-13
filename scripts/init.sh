#!/bin/bash

#apt update -y && apt upgrade -y
#apt install openvpn wireguard python3-pip -y
#
#curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
#export NVM_DIR="$HOME/.nvm"
#[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
#[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
#nvm install 20
#
#npm install pm2 -g
pip install -r requirements.txt

pm2 start main.py --interpreter=python3 -- wg_agent
pm2 start main.py --interpreter=python3 -- ovpn_agent
pm2 start main.py --interpreter=python3 -- uptime_agent
pm2 start main.py --interpreter=python3 -- subscription_agent
