#!/bin/bash

sudo dnf autoremove
sudo dnf clean all
sudo dnf upgrade -y

flatpak uninstall --unused
flatpak repair
flatpak update -y

sudo snap refresh
sudo rm -rf /var/lib/snapd/cache/*
