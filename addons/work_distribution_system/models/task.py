from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

#Extends the base task class
class Task(models.Model):
    _inherit  = 'project.task'

    #Data fields
    name = fields.Char(default='Oggetto mail')
    status = fields.Char(string='Stato', compute='compute_status')
    deptm = fields.Char(string='Dipartimento', default='Generale')
    arrive_date = fields.Datetime(string='Data e ora di arrivo', default=fields.Datetime.now())
    mail_sender = fields.Text(string='Mittente', default='sender@email.com')
    mail_subject = fields.Text(string='Oggetto', default='Oggetto mail')
    mail_body = fields.Html(string='Corpo', default='<p>Nessun corpo presente</p>')
    mail_attach_count = fields.Integer(string='Numero di allegati', compute='get_attachments_count')
    mail_attach_ids = fields.One2many(
        'ir.attachment',
        'res_id',
        domain=[('res_model', '=', 'project.task')],
        string='Allegati'
    )
    active = fields.Boolean(default=True)

    #Called when a new email comes in and needs to be converted into a task
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
    
    #Called when a reply to an email comes in and the relative task needs to be updated
    @api.model
    def message_update(self, msg_dict, update_vals=None):
        update_vals = update_vals or {}
        update_vals.update({
            'mail_body': msg_dict.get('body', '')
        })

        return super().message_update(msg_dict, update_vals)

    #Returns status (needed because otherwise odoo throws an error because of hiding the default field)
    @api.depends('stage_id')
    def compute_status(self):
        for task in self:
            task.status = task.stage_id.name if task.stage_id else ''

    #Returns a dictionary of the attachments
    @api.depends('message_ids')
    def get_attachments(self):
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'project.task'),
            ('res_id', '=', self.id)
        ])

        return attachments

    #Sets the attachment count
    @api.depends('message_ids') 
    def get_attachments_count(self):
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'project.task'),
            ('res_id', '=', self.id)
        ])

        self.mail_attach_count = len(attachments)

    #WRONG: don't use
    def download_all_attachments(self):
        atchmts = self.get_attachments()
        for file in atchmts:
            file.action_download()

    def save_changes(self):
        pass

    def send_response_it(self):
        pass

    def send_response_eng(self):
        pass

    def archive_task(self):
        self.write({'active': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }

    def unarchive_task(self):
        self.write({'active': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }

    def delete_task(self):
        project = self.project_id

        #Delete the attachments
        attachments = self.get_attachments()
        attachments.unlink()

        super().unlink()