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
    is_read = fields.Boolean(default=False)
    is_deleted = fields.Boolean(string='Nel cestino', default=False)
    is_deleted_date = fields.Datetime(string='Data eliminazione')

    #Mark task as opened
    def mark_read(self):
        _logger.info("mark_read called for tasks: %s", self.ids)
        unread = self.filtered(lambda t: not t.is_read)
        _logger.info("unread tasks: %s", unread.ids)
        if unread:
            unread.write({'is_read': True})
            return True
        return False

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
        
        task = super().message_new(msg_dict, custom_values)

        # Notify clients via bus
        '''self.env['bus.bus']._sendone(
            'notify',
            'new_task',
            {'task_id': task.id}
        )'''            #Not used cause bus events won't work from the frontend for some reason

        return task
    
    #Called when a reply to an email comes in and the relative task needs to be updated, appends the new body to the old one
    @api.model
    def message_update(self, msg_dict, update_vals=None):
        update_vals = update_vals or {}
        new_body = msg_dict.get('body', '')
        current_body = self.mail_body or ''

        update_vals.update({
            'mail_body': current_body + '<hr/>' + new_body
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
        #Not really needed since there's autosave, still here for UX
        pass

    #Usa un template ed invia una mail di risposta
    def send_response_it(self):
        template = self.env.ref('work_distribution_system.email_template_response_it')
        template.send_mail(self.id, force_send=True)

    #Usa un template ed invia una mail di risposta
    def send_response_eng(self):
        template = self.env.ref('work_distribution_system.email_template_response_en')
        template.send_mail(self.id, force_send=True)

    #Uses ODOO's default system by modifying the "active" parameter
    def archive_task(self):
        self.write({'active': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }

    #Uses ODOO's default system by modifying the "active" parameter
    def unarchive_task(self):
        self.write({'active': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }
    
    #Moves task to deleted bin
    def move_to_bin_task(self):
        self.write({
            'is_deleted': True,
            'is_deleted_date': fields.Datetime.now(),
            'active': False  
        })
        return {'type': 'ir.actions.act_window_close'}
    
    #Clears bin
    def empty_bin(self):
        deleted_tasks = self.with_context(active_test=False).search([
            ('is_deleted', '=', True),
        ])
        deleted_tasks.unlink()

    #Moves the task OUT of the bin
    def restore_task(self):
        self.write({
            'is_deleted': False,
            #'is_deleted_date': fields.Datetime.now(),
            'active': True  
        })

    #Deletes PERMANENTLY the task and its attachments, but it's not shown visually
    def delete_task(self):
        project = self.project_id

        #Delete the attachments
        attachments = self.get_attachments()
        attachments.unlink()

        super().unlink()

    #Print task with custom view
    def print_task(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'action_print',
            'params': {}
        }

    #Called by a cron job. It checks if the tasks is older than a certain threshold and if so it archives it
    @api.model
    def check_date_archive(self):
        tasks = self.search([
            ('arrive_date', '!=', False),
            ('active', '=', True)
        ])

        for task in tasks:
            delta = fields.Datetime.now() - task.arrive_date
            hours = delta.total_seconds() / 3600
            years = delta.total_seconds() / 31536000    #exactly one year
            
            #if(hours > 24):
            if(years > 5):
                task.archive_task()

    #Called by a cron job. It checks if the tasks is older than a certain threshold and if so it deletes it
    @api.model
    def check_date_delete(self):
        tasks = self.search([
            ('arrive_date', '!=', False),
            ('active', '=', True)
        ])

        for task in tasks:
            delta = fields.Datetime.now() - task.arrive_date
            hours = delta.total_seconds() / 3600
            years = delta.total_seconds() / 31536000    #exactly one year
            
            #if(hours > 24):
            if(years > 5 and not task.active):  #Archived tasks don't get deleted
                task.delete_task()