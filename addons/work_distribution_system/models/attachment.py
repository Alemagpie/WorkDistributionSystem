from odoo import models

#Extension of file attachment
class IrAttachment(models.Model):
    _inherit='ir.attachment'

    #Called when download button is pressed
    def action_download(self):
        #Ensures only one record is passed
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self.id}?download=true',
            'target': 'self'
        }