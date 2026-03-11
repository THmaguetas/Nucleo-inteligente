#!/bin/bash

mount /dev/sdb /media/projs_Ti

mount /dev/sdc /media/arquivos

mount -o uid=$(id -u),gid=$(id -g),umask=022 /dev/sdd1 /media/dados
