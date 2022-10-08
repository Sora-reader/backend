#!/usr/bin/env bash

info "Debug mode" "Installing dependencies"
sudo chown sora:sora ~/.cache/pypoetry/
poetry install

./scripts/entrypoint.sh