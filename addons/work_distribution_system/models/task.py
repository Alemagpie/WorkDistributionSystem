from odoo import models, fields

class Task(models.Model):
    _inherit  = 'project.task'

    test_field = fields.Char(string='Test Field')
    test_text = fields.Text(string='Default text', default = 'Custom text')

    #Fields:
        #id (from primary key)
        #status (from stage_id)
        #priority
        #creation date (create_date)
        #arrive date
        #deadline
        #last update (from write_time)
        #department (0,1)
        #sender 
        #object
        #body
        #attachments

    #Functions:
        #Delete
        #Archive
        #Automatic response (it)
        #Automatic response (eng)