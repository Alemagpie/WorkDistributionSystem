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
    mail_body = fields.Html(string='Corpo', default='<h1>Title</h1><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent ultricies sed urna ac tincidunt. Integer non erat ut sem pretium tempor scelerisque et nibh. Fusce bibendum consequat massa, sit amet facilisis mi posuere ut. Mauris posuere accumsan auctor. Duis ornare leo sed justo venenatis accumsan in a dui. Cras varius mollis nibh vitae commodo. Fusce hendrerit est et ipsum sagittis consectetur. Proin odio purus, pulvinar sed hendrerit nec, rutrum nec turpis. Maecenas eget tempus orci. Cras tempus metus ligula, nec viverra ipsum sodales a. Proin iaculis a nunc et tincidunt. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Phasellus sed ligula scelerisque, viverra nulla non, molestie arcu. Curabitur at diam in lacus eleifend malesuada. Ut lobortis, ex vitae auctor accumsan, velit lacus ornare erat, at porta nisi massa vel lectus. Duis lorem eros, pharetra quis libero et, ullamcorper vestibulum neque. Etiam mauris metus, tempus a ligula a, venenatis consequat dolor. Vivamus mollis at eros eget bibendum. Aliquam maximus facilisis quam, a hendrerit leo faucibus sit amet. Proin aliquet quam at vestibulum rutrum. Suspendisse libero ex, accumsan nec enim vel, auctor mattis ante. Mauris egestas lacinia sapien, et tristique lorem volutpat eu. Nunc laoreet, nunc condimentum consectetur cursus, diam elit maximus dolor, eu molestie neque lectus id lectus. Nulla convallis, turpis eu mollis congue, erat lacus dapibus mi, ut ultricies neque ligula vel augue. Fusce sed maximus enim, sit amet pharetra nibh. Donec ac neque cursus, porttitor urna et, aliquam neque. Ut vestibulum tortor eu velit dapibus placerat. Praesent pharetra eros velit, at laoreet magna condimentum ut. Integer tincidunt euismod auctor. Praesent eget suscipit nulla. In a libero at ligula fringilla scelerisque id volutpat dolor. Nunc venenatis molestie ante, a iaculis augue venenatis non. Proin vel diam non arcu semper gravida.</p>')
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

    def save_changes(self):
        pass

    def send_response_it(self):
        pass

    def send_response_eng(self):
        pass

    def _set_from_mail(self, sender, subj, body):
        self.mail_sender = sender
        self.name = subj
        self.mail_object = subj
        self.mail_body = body