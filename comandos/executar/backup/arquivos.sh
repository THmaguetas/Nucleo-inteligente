#!/bin/bash

BACKUP="/media/backups"
LOG="/tmp/backup_$(date +%Y-%m-%d_%H-%M-%S).log"

if ! mountpoint -q "$BACKUP"; then
    echo "|≻ Montando $BACKUP" | tee -a "$LOG"
    sudo mount /dev/sdd2 "$BACKUP" || { echo "$BACKUP nao montado"; exit 1; }
fi
mountpoint -q "$BACKUP" || { echo "Backup nao montado, deu pau"; exit 1; }


echo "|≻ Backup Obsidian" | tee -a "$LOG"
rsync -avh --delete --ignore-errors --inplace \
    --no-perms --no-owner --no-group \
    /media/arquivos/obsidian/ "$BACKUP/backup_arquivos/obsidian" >> "$LOG" 2>&1

echo "|≻ Backup Projetos" | tee -a "$LOG"
rsync -avh --delete --ignore-errors --inplace \
    --no-perms --no-owner --no-group \
    /media/projs_Ti/Codigos/ "$BACKUP/backup_arquivos/Codigos" >> "$LOG" 2>&1

echo "|≻ Backup Fotos e Vídeos" | tee -a "$LOG"
rsync -avh --delete --ignore-errors --inplace \
    --no-perms --no-owner --no-group \
    /media/arquivos/fotos_e_videos/ "$BACKUP/backup_arquivos/fotos_e_videos" >> "$LOG" 2>&1


echo "|≻ Desmontando $BACKUP" | tee -a "$LOG"
sudo umount -l "$BACKUP" || echo "deu pau pra desmontar $BACKUP" | tee -a "$LOG"

echo "=== Fim do backup em $(date) ===" | tee -a "$LOG"
echo "Log salvo em $LOG"
