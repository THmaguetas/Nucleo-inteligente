#!/bin/bash

BACKUP="/media/backups"
LOG="/tmp/backup_$(date +%Y-%m-%d_%H-%M-%S).log"

if ! mountpoint -q "$BACKUP"; then
    echo "|≻ Montando $BACKUP" | tee -a "$LOG"
    sudo mount /dev/sdd2 "$BACKUP" || { echo "$BACKUP nao montado"; exit 1; }
fi
mountpoint -q "$BACKUP" || { echo "Backup nao montado, deu pau"; exit 1; }


echo "|≻ Backup TH survival" | tee -a "$LOG"
rsync -avh --delete --ignore-errors --inplace \
    --no-perms --no-owner --no-group \
    /home/th/.minecraft/saves/ "$BACKUP/backup_minecraft/mundos_salvos/" >> "$LOG" 2>&1


echo "|≻ Desmontando $BACKUP" | tee -a "$LOG"
sudo umount -l "$BACKUP" || echo "deu pau pra desmontar $BACKUP" | tee -a "$LOG"

echo "=== Fim do backup em $(date) ===" | tee -a "$LOG"
echo "Log salvo em $LOG"
