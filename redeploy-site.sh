#!/bin/sh

pkill -f tmux

cd ~/MLH-portfolio-website

git fetch && git reset origin/main --hard

python -m venv python3-virtualenv

source python3-virtualenv/bin/activate

pip install -r requirements.txt

tmux new-session -d -s mlh-portolfio-website-server 'cd ~/MLH-portfolio-website && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'

echo "Site has successfully been redeployed! :)"
