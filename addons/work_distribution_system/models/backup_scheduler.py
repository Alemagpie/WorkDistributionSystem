import os
import base64
from datetime import datetime
from odoo import models, api
import odoo.service.db as db_service

class BackupScheduler(models.Model):
    _name = 'backup.scheduler'

    @api.model
    def backup(self):
        backup_dir = '/var/lib/odoo/backups'
        os.makedirs(backup_dir, exist_ok= True)

        date = datetime.now().strftime('%Y-%m-%d_%H-%M')
        db_name = self.env.cr.dbname
        filename = f'{backup_dir}/{db_name}.zip'

        #ODOO's internal api
        backup_data = db_service.dump_db(db_name, None, 'zip')

        with open(filename, 'wb') as file:
            file.write(backup_data.read())

        for file in os.listdir(backup_dir):
            filepath = os.path.join(backup_dir, file)
            # Remove older backups. If a backup was modified withing 7 days it won't get deleted
            if os.path.getmtime(filepath) < (datetime.now().timestamp() - 7 * 86400):
                os.remove(filepath)