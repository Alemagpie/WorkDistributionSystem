from odoo import models, fields, api

class Task(models.Model):
    _inherit  = 'project.task'

    status = fields.Char(string='Stato', compute='_compute_status')
    deptm = fields.Char(string='Dipartimento', default='Generale')
    arrive_date = fields.Datetime(string='Data e ora di arrivo')
    mail_sender = fields.Text(string='Mittente', default='alessio.fagnani@studenti.unipd.it')
    mail_object = fields.Text(string='Oggetto', default='Tirocinio')
    mail_body = fields.Text(string='Corpo', default='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')
    #mail_attach = ...

    test_field = fields.Char(string='Test Field')
    test_text = fields.Text(string='Default text', default = 'Custom text')

    #Fields:
        #id (from id)                       ✔

        #status (from stage_id)             ✔
        #priority                           ✔
        #deadline (from date_deadline)      ✔
        #department (0,1)                   X

        #arrive date                        ✔
        #creation date (from create_date)   ✔
        #last update (from write_time)      ✔

        #sender 
        #object
        #body
        #attachments

    #Functions:
        #Delete
        #Archive
        #Automatic response (it)
        #Automatic response (eng)

    @api.depends('stage_id')
    def _compute_status(self):
        for task in self:
            task.status = task.stage_id.name if task.stage_id else ''