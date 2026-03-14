#!/bin/bash

tema_escolhido="${1:-}"

diret_base="$HOME/.config/Hypr_rice-th"
diret_tema="$diret_base/themes/$tema_escolhido"

# vê se o tema existe ou n
[[ -d "$diret_tema" ]] || { echo "esse tema não existe caraio"; exit 1; }

# -=- troca de tema por links simbólicos -=-
ln -sf "$diret_tema/nemo.css"      "$diret_base/nemo/gtk-3.0/nemo.css"
ln -sf "$diret_tema/central.css"   "$diret_base/TH_controle/gerenciador_de_energia/central.css"
ln -sf "$diret_tema/waybar.css"    "$diret_base/waybar/waybar.css"
ln -sf "$diret_tema/wofi.css"      "$diret_base/wofi/wofi.css"

ln -sf "$diret_tema/border.conf"   "$diret_base/hypr/modulos_hypr/border.conf"
ln -sf "$diret_tema/kitty.conf"    "$diret_base/kitty/kitty.conf"
ln -sf "$diret_tema/mako.conf"     "$diret_base/mako/mako.conf"

ln -sf "$diret_tema/wallpaper.jpg" "$diret_base/hypr/wallpaper/wallpaper.jpg"

# reload da interface
pkill waybar
pkill hyprpaper
pkill -USR1 kitty
pkill mako 

waybar &
mako &
kitty @ set-colors --all "$diret_tema/kitty.conf"
hyprpaper &

hyprctl reload
