#!/bin/sh

pkill -f tmux

cd ~/MLH-portfolio-website

git fetch && git reset origin/main --hard 

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build

echo "Site has been deployed successfully! :)"



