#!/usr/bin/env bash

# Script to redeploy data stuff and rq worker. Used by server's webhook server on push

git fetch --all
git reset --hard "origin/$(git branch --show-current)"

cd ..
docker-compose --profile prod-partial up -d --build