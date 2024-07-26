#!/bin/sh

pkill -f tmux

cd ~/MLH-portfolio-website

git fetch && git reset origin/main --hard || exit 1

docker-compose -f docker-compose.prod.yml down || exit 1

docker-compose -f docker-compose.prod.yml up -d --build || exit 1

docker-compose -f docker-compose.prod.yml ps