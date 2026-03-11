#!/bin/bash 

echo "|≻ começando limpeza do sistema"

set -e

# arquivos temp
rm -rf /tmp/*
rm -rf /var/tmp/*

# lixeira
rm -rf ~/.local/share/Trash/*
rm -rf /run/media/$USER/*/.Trash-*/*

# cache
rm -rf ~/.cache/*

# dnf flat e snap
dnf clean all
flatpak uninstall --unused
rm -rf /var/lib/snapd/cache/*

# logs do sistema
find /var/log -type f \( -name "*.gz" -o -name "*.old" \) -delete
journalctl --vacuum-size=100M

echo "|≻ limpeza finalizada"
