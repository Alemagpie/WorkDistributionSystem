from odoo import models, fields, api
from odoo.osv import expression
from datetime import timedelta
from collections import Counter
import io
import os
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
    is_assigned_to_me = fields.Boolean(string='Assegnato a me', compute='compute_is_assigned_to_me')

    #-----------------------------------------------------------------------------------------------

    #Overrides the search function to not included tasks marked as deleted
    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if not self._context.get('show_deleted'):
            domain = expression.AND([[('is_deleted', '=', False)], domain])
        return super()._search(domain, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)

    #Called both by the backend to fetch data and when user opens task
    def read(self, fields=None, load='_classic_read'):
        result = super().read(fields, load)
        if len(self) == 1 and not self.env.context.get('no_mark_read'):
            if not self.is_read:
                self.with_context(no_mark_read=True).write({
                    'is_read': True,
                    'color': 0
                    })
        return result

    #Mark task as opened
    def mark_read(self):
        unread = self.filtered(lambda t: not t.is_read)
        if unread:
            unread.write({'is_read': True})
            return True
        return False

    #Called when a new email comes in and needs to be converted into a task
    @api.model
    def message_new(self, msg_dict, custom_values=None):
        subject = msg_dict.get('subject', '')
        body = msg_dict.get('body', '')

        if(not self.filter_mail(subject, body)):
            return

        custom_values = custom_values or {}
        custom_values.update({
            'name': msg_dict.get('subject', '*Nessun oggetto*'),
            'mail_subject': msg_dict.get('subject', ''),
            'mail_sender': msg_dict.get('email_from', ''),
            'mail_body': msg_dict.get('body', ''),
            'arrive_date': msg_dict.get('date', fields.Datetime.now()),
            'is_read': False,
            'color': 1
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
    
    #Removes user from being assigned to task
    def unassign_task(self):
        '''self.write({
            'user_ids': [(3, self.env.user.id)]
        })'''
        self.user_ids = [(3, self.env.user.id)]

    #Returns status (needed because otherwise odoo throws an error because of hiding the default field)
    @api.depends('stage_id')
    def compute_status(self):
        for task in self:
            task.status = task.stage_id.name if task.stage_id else ''

    @api.depends('user_ids')
    def compute_is_assigned_to_me(self):
        for task in self:
            task.is_assigned_to_me = self.env.user in task.user_ids

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
    
    #Navigate to bin menu
    def open_bin(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cestino',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('is_deleted', '=', True)],
            'context': {'show_deleted': True},
            'views': [
                (self.env.ref('work_distribution_system.project_task_bin_list').id, 'tree'),
                (False, 'form'),  # False means use default form view
            ]
        }
    
    #Moves task to deleted bin
    def move_to_bin_task(self):
        self.write({
            'is_deleted': True,
            'is_deleted_date': fields.Datetime.now()
        })

        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }
    
    #Clears bin
    def empty_bin(self):
        deleted_tasks = self.with_context(show_deleted=True).search([
        ('is_deleted', '=', True)
        ])

        for task in deleted_tasks:
            attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'project.task'),
                ('res_id', '=', task.id)
            ])
            attachments.unlink()
        deleted_tasks.unlink()

    #Moves the task OUT of the bin
    def restore_task(self):
        self.write({
            'is_deleted': False,
            'is_deleted_date': fields.Datetime.now() 
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }
    
    def restore_task_no_reload(self):
        self.write({
            'is_deleted': False,
            'is_deleted_date': fields.Datetime.now() 
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
    
    #-----------------------------------------------------------------------------------------------

    #Returns filter set from system parameters (set in ODOO app)
    @api.model
    def get_filter_words(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'work_distribution_system.words_filter', ''
        )
        return frozenset(w.strip().lower() for w in param.split(',') if w.strip())

    #Filters mail based on set words
    @api.model
    def filter_mail(self, subject, body):
        words = self.get_filter_words()
        if not words:
            return True
        subject_lc = subject.lower()
        body_lc = body.lower()

        return not any(
            word in subject_lc or word in body_lc
            for word in words
        )


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

    #Called once a month, creates a summary of last month's tasks based on their tags
    @api.model
    def generate_monthly_summary(self):
        today = fields.Date.today()
        first_day = today.replace(day=1)
        last_month_end = first_day - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        tasks = self.with_context(show_deleted=True).search([
            ('create_date', '>=', last_month_start),
            ('create_date', '<=', last_month_end),
        ])

        # Count tasks per tag
        tag_counter = Counter()
        no_tag_count = 0

        for task in tasks:
            if task.tag_ids:
                for tag in task.tag_ids:
                    tag_counter[tag.name] += 1
            else:
                no_tag_count += 1

        import locale
        try:
            locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
        except:
            pass
        
        month_year = last_month_start.strftime('%B %Y').capitalize()
        filename = last_month_start.strftime('%B-%Y').capitalize()

        # Build txt — style however you want
        lines = []
        lines.append('=' * 40)
        lines.append(f'  RIEPILOGO MENSILE - {month_year}')
        lines.append('=' * 40)
        lines.append('')
        lines.append(f'{"ETICHETTA":<25} {"N. TASK":>10}')
        lines.append('-' * 40)
        
        for tag_name, count in sorted(tag_counter.items()):
            lines.append(f'{tag_name:<25} {count:>10}')
        
        if no_tag_count:
            lines.append(f'{"Senza etichetta":<25} {no_tag_count:>10}')
        
        lines.append('-' * 40)
        lines.append(f'{"TOTALE":<25} {sum(tag_counter.values()) + no_tag_count:>10}')
        lines.append('=' * 40)

        content = '\n'.join(lines)

        summary_dir = '/mnt/summaries'
        os.makedirs(summary_dir, exist_ok=True)
        filepath = os.path.join(summary_dir, f'{filename}.txt')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)