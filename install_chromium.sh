#!/bin/bash
set -e

apt-get update
apt-get install -y chromium chromium-driver

# Exibe o caminho do Chromium para debug
which chromium
which chromium-browser || true
which chromium-driver 