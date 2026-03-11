#!/bin/bash

BACKUP="/media/backups"
LOG="/tmp/backup_$(date +%Y-%m-%d_%H-%M-%S).log"

if ! mountpoint -q "$BACKUP"; then
    echo "|≻ Montando $BACKUP" | tee -a "$LOG"
    sudo mount /dev/sdd2 "$BACKUP" || { echo "$BACKUP nao montado"; exit 1; }
fi
mountpoint -q "$BACKUP" || { echo "Backup nao montado, deu pau"; exit 1; }


echo "|≻ Backup /home/th/Documentos" | tee -a "$LOG"
rsync -avh --delete --ignore-errors --inplace \
    --no-perms --no-owner --no-group \
    /home/th/Documentos "$BACKUP/config_linux/Documents" >> "$LOG" 2>&1


echo "|≻ Backup .config/Hypr_rice-th" | tee -a "$LOG"
rsync -avh --delete --ignore-errors --inplace \
    --no-perms --no-owner --no-group \
    /home/th/.config/Hypr_rice-th "$BACKUP/config_linux/rice-th" >> "$LOG" 2>&1


echo "|≻ Desmontando $BACKUP" | tee -a "$LOG"
sudo umount -l "$BACKUP" || echo "deu pau pra desmontar $BACKUP" | tee -a "$LOG"

echo "=== Fim do backup em $(date) ===" | tee -a "$LOG"
echo "Log salvo em $LOG"
