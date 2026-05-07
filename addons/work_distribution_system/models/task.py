from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class Task(models.Model):
    _inherit  = 'project.task'

    name = fields.Char(default='Oggetto mail')
    status = fields.Char(string='Stato', compute='_compute_status')
    deptm = fields.Char(string='Dipartimento', default='Generale')
    arrive_date = fields.Datetime(string='Data e ora di arrivo', default=fields.Datetime.now())
    mail_sender = fields.Text(string='Mittente', default='sender@email.com')
    mail_subject = fields.Text(string='Oggetto', default='Oggetto mail')
    mail_body = fields.Html(string='Corpo', default='<p>Nessun corpo presente</p>')
    mail_attach_count = fields.Char(string='Numero di allegati', default='1')

    #Fields:
        #id (from id)                       ✔

        #status (from stage_id)             ✔
        #priority                           ✔
        #deadline (from date_deadline)      ✔
        #department (0,1)                   X

        #arrive date                        ✔
        #creation date (from create_date)   ✔
        #last update (from write_time)      ✔

        #sender                             ✔
        #object                             ✔
        #body                               ✔
        #attachments                        X

    #Functions:
        #Delete
        #Archive
        #Automatic response (it)
        #Automatic response (eng)

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        custom_values = custom_values or {}
        custom_values.update({
            'name': msg_dict.get('subject', '*Nessun oggetto*'),
            'mail_subject': msg_dict.get('subject', ''),
            'mail_sender': msg_dict.get('email_from', ''),
            'mail_body': msg_dict.get('body', ''),
            'arrive_date': msg_dict.get('date', fields.Datetime.now())
        })
        
        return super().message_new(msg_dict, custom_values)
    
    @api.model
    def message_update(self, msg_dict, update_vals=None):
        update_vals = update_vals or {}
        update_vals.update({
            'mail_body': msg_dict.get('body', '')
        })

        return super().message_update(msg_dict, update_vals)

    @api.depends('stage_id')
    def _compute_status(self):
        for task in self:
            task.status = task.stage_id.name if task.stage_id else ''

    def download_attachments(self):
        pass

    def save_changes(self):
        pass

    def send_response_it(self):
        pass

    def send_response_eng(self):
        pass

    def archive_task(self):
        pass

    def delete_task(self):
        pass

    def _set_from_mail(self, sender, subj, body):
        self.mail_sender = sender
        self.name = subj
        self.mail_object = subj
        self.mail_body = body