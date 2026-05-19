#!/bin/bash

# DO NOT USE, ODOO WILL BLOCK ANY EXTERNAL API CALL

source ../.env

BACKUP_DIR = "../backups"
ODOO_DB = "odoo"
ADMIN_PASSWORD = ${POSTGRES_PASSWORD}

# -p flags tells it not to throw error if it already exists. Here for redundancy
mkdir -p ${BACKUP_DIR}

# create the backup from odoo's endpoint
# \ => command continues on the next line
# -F => send as form field, -o => specifies output file
curl -X POST \
    -F "master_pwd=${ADMIN_PASSWORD}" \
    -F "name=${ODOO_DB}" \
    -F "backup_format=zip" \
    -o ${BACKUP_DIR}/$(date +%F).zip \
    http://localhost:8069/web/database/manager

# delete old backups
# -type f => only files, -mtime +2 => older than 2 days
find ${BACKUP_DIR} -type f -mtime +2 -name "*.zip" -delete



# Create cron job with this file:
# sudo chmod +x ./src/backup_linux.sh
# crontab -e
# 30 1 * * * ./backup_linux.sh