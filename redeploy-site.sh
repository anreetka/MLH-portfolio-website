#!/bin/sh

pkill -f tmux

cd ~/MLH-portfolio-website

git fetch && git reset origin/main --hard

python -m venv python3-virtualenv

source python3-virtualenv/bin/activate

pip install -r requirements.txt

systemctl daemon-reload

systemctl restart myportfolio

echo "Site has successfully been redeployed! :)"
