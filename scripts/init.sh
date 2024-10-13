#!/bin/bash

if [ -s "$NVM_DIR/nvm.sh" ]; then
    echo "NVM установлен."
else
    apt update -y && apt upgrade -y
    apt install openvpn wireguard python3-pip resolvconf -y
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
    nvm install 20
    npm install pm2 -g
fi


pip install -r requirements.txt

pm2 start main.py --interpreter python3 --name "wg_agent" -f -- wg_agent
pm2 start main.py --interpreter python3 --name "ovpn_agent" -f -- ovpn_agent
pm2 start main.py --interpreter python3 --name "uptime_agent" -f -- uptime_agent
pm2 start main.py --interpreter python3 --name "subscription_agent" -f -- subscription_agent